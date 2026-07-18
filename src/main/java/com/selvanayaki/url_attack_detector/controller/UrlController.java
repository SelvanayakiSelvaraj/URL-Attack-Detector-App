package com.selvanayaki.url_attack_detector.controller;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.selvanayaki.url_attack_detector.model.ScanHistory;
import com.selvanayaki.url_attack_detector.model.User;
import com.selvanayaki.url_attack_detector.repository.ScanHistoryRepository;
import com.selvanayaki.url_attack_detector.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

@RestController
@CrossOrigin(origins = "*")
public class UrlController {

    @Value("${ml.api.url}")
    private String mlApiUrl;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private ScanHistoryRepository scanHistoryRepository;

    @GetMapping("/analyze-url")
    public ResponseEntity<?> analyzeUrl(
            @RequestParam(name = "url") String url,
            @RequestParam(name = "userId", required = false) Long userId) {

        try {
            // 1. Extract IP Address of the target URL
            String ipAddress = "Unknown";
            try {
                URL parsedUrl = new URL(url);
                ipAddress = java.net.InetAddress.getByName(parsedUrl.getHost()).getHostAddress();
            } catch (Exception ignored) {}

            // ... proceed with Python ML call
            String jsonPayload = "{\"url\": \"" + url.replace("\"", "\\\"") + "\"}";
            URL obj = new URL(mlApiUrl);
            HttpURLConnection con = (HttpURLConnection) obj.openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("Content-Type", "application/json");
            con.setConnectTimeout(10000);
            con.setReadTimeout(10000);
            con.setDoOutput(true);

            try (OutputStream os = con.getOutputStream()) {
                byte[] input = jsonPayload.getBytes("utf-8");
                os.write(input, 0, input.length);
            }

            int responseCode = con.getResponseCode();

            BufferedReader in;
            if (responseCode >= 200 && responseCode <= 299) {
                in = new BufferedReader(new InputStreamReader(con.getInputStream()));
            } else {
                in = new BufferedReader(new InputStreamReader(con.getErrorStream()));
            }

            String inputLine;
            StringBuilder response = new StringBuilder();
            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();

            String responseString = response.toString();
            ObjectMapper mapper = new ObjectMapper();
            
            // Re-parse the response to add IP Address
            com.fasterxml.jackson.databind.node.ObjectNode jsonResponse;
            try {
                jsonResponse = (com.fasterxml.jackson.databind.node.ObjectNode) mapper.readTree(responseString);
            } catch (Exception ex) {
                // If it fails to parse as JSON, it's likely an HTML error page from Render or Flask.
                // We truncate it to 200 chars so it fits in the error message.
                String snippet = responseString.length() > 200 ? responseString.substring(0, 200) + "..." : responseString;
                throw new Exception("ML Service returned non-JSON response (HTTP " + responseCode + "): " + snippet);
            }
            jsonResponse.put("ip_address", ipAddress);
            responseString = jsonResponse.toString();

            // Parse prediction and save history if user is logged in
            if (responseCode >= 200 && responseCode <= 299 && userId != null) {
                try {
                    String prediction = jsonResponse.has("prediction") ? jsonResponse.get("prediction").asText() : "Unknown";
                    String attackType = jsonResponse.has("attack_type") ? jsonResponse.get("attack_type").asText() : "None";
                    String riskLevel = jsonResponse.has("risk_level") ? jsonResponse.get("risk_level").asText() : "Unknown";

                    Optional<User> userOpt = userRepository.findById(userId);
                    if (userOpt.isPresent()) {
                        ScanHistory history = new ScanHistory(url, prediction, attackType, riskLevel, userOpt.get());
                        scanHistoryRepository.save(history);
                    }
                } catch (Exception parseEx) {
                    System.err.println("Failed to save history: " + parseEx.getMessage());
                }
            }

            return ResponseEntity.status(responseCode)
                    .contentType(org.springframework.http.MediaType.APPLICATION_JSON)
                    .body(responseString);

        } catch (Exception e) {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("error", "Failed to connect to ML service: " + e.getMessage());
            errorResponse.put("url", url);
            errorResponse.put("ip_address", "Unknown");
            errorResponse.put("prediction", "Unknown");
            errorResponse.put("attack_type", "None");
            errorResponse.put("risk_level", "Unknown");
            return ResponseEntity.status(500).body(errorResponse);
        }
    }

    @PostMapping("/api/url/save-history")
    public ResponseEntity<?> saveHistory(@RequestBody java.util.Map<String, Object> payload) {
        try {
            Long userId = payload.containsKey("userId") ? Long.parseLong(payload.get("userId").toString()) : null;
            if (userId == null) {
                return ResponseEntity.badRequest().body(java.util.Map.of("error", "User ID is required"));
            }

            String url = payload.getOrDefault("url", "Unknown").toString();
            String prediction = payload.getOrDefault("prediction", "Unknown").toString();
            String attackType = payload.getOrDefault("attack_type", "None").toString();
            String riskLevel = payload.getOrDefault("risk_level", "Unknown").toString();

            Optional<User> userOpt = userRepository.findById(userId);
            if (userOpt.isPresent()) {
                ScanHistory history = new ScanHistory(url, prediction, attackType, riskLevel, userOpt.get());
                scanHistoryRepository.save(history);
                return ResponseEntity.ok(java.util.Map.of("message", "History saved successfully"));
            } else {
                return ResponseEntity.status(404).body(java.util.Map.of("error", "User not found"));
            }
        } catch (Exception e) {
            return ResponseEntity.status(500).body(java.util.Map.of("error", "Failed to save history: " + e.getMessage()));
        }
    }
}

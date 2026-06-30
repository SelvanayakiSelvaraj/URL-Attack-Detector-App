package com.selvanayaki.url_attack_detector.controller;

import com.selvanayaki.url_attack_detector.model.ScanHistory;
import com.selvanayaki.url_attack_detector.repository.ScanHistoryRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/history")
@CrossOrigin(origins = "*")
public class HistoryController {

    @Autowired
    private ScanHistoryRepository scanHistoryRepository;

    @GetMapping("/{userId}")
    public ResponseEntity<?> getUserHistory(@PathVariable("userId") String userId) {
        try {
            Long uid = Long.parseLong(userId);
            List<ScanHistory> history = scanHistoryRepository.findByUserIdOrderByScannedAtDesc(uid);
            return ResponseEntity.ok(history);
        } catch (NumberFormatException nfe) {
            return ResponseEntity.badRequest().body(java.util.Map.of("error", "Invalid User ID format"));
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(500).body(java.util.Map.of("error", "Failed fetching from DB: " + e.getMessage()));
        }
    }
}

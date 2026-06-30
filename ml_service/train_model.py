import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import os

def create_model():
    print("Generating sample dataset...")
    # Sample data containing various attack types
    data = {
        'url': [
            # --- SAFE URLS (Ensuring Google and others are Safe) ---
            'https://www.google.com',
            'https://www.google.com/search?q=machine+learning',
            'https://www.google.com/search?q=weather+today',
            'https://www.bing.com',
            'https://duckduckgo.com',
            'https://github.com',
            'https://github.com/trending',
            'https://www.linkedin.com/feed/',
            'https://www.facebook.com',
            'https://www.instagram.com',
            'https://twitter.com/home',
            'https://www.youtube.com',
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://en.wikipedia.org/wiki/Main_Page',
            'https://www.amazon.com',
            'https://www.netflix.com',
            'https://www.reddit.com/r/python',
            'https://stackoverflow.com/questions',
            'https://www.medium.com',
            'https://www.nytimes.com',
            'https://www.bbc.com/news',
            'https://www.cnn.com',
            'https://www.apple.com',
            'https://www.microsoft.com',
            'https://www.adobe.com',
            'https://www.spotify.com',
            'https://www.zoom.us',
            'https://www.slack.com',
            'https://www.coursera.org',
            'https://www.udemy.com',
            'https://www.khanacademy.org',
            'https://www.trello.com',
            'https://www.notion.so',
            'https://www.canva.com',
            'https://www.dropbox.com',
            'https://www.paypal.com',
            'https://www.stripe.com',
            'https://www.heroku.com',
            'https://www.digitalocean.com',
            'https://www.cloudflare.com',

            # --- SQL INJECTION ATTACKS ---
            'http://test.com/login?user=admin\' OR \'1\'=\'1',
            'http://shop.com/item?id=5 OR 1=1',
            'http://site.com/search?q=1\' UNION SELECT 1,2,3--',
            'http://db.com/data?id=-1\' UNION SELECT username, password FROM users--',
            'http://bank.com/transfer?acct=123; DROP TABLE transactions--',
            'http://test.com/profile?id=1\' AND SLEEP(5)--',
            'http://site.com/?user=admin\' #',
            'http://api.com/v1/user?name=admin\'-- -',
            'http://test.com/search?id=1" OR "1"="1',
            'http://shop.com/item?id=1 UNION ALL SELECT NULL,NULL,NULL,NULL--',
            'http://db.com/users?id=1\' AND (SELECT 1 FROM (SELECT(SLEEP(5)))a)--',
            'http://site.com/products?cat=1\' AND 1=2 UNION SELECT (SELECT table_name FROM information_schema.tables LIMIT 0,1),2,3--',

            # --- CROSS-SITE SCRIPTING (XSS) ---
            'http://bad.com/<script>alert("XSS")</script>',
            'http://site.com/search?q=<img src=x onerror=alert(1)>',
            'http://app.com/?redirect=javascript:alert(1)',
            'http://test.com/message?msg=<svg/onload=alert(1)>',
            'http://site.com/comment?text=<iframe src="javascript:alert(1)"></iframe>',
            'http://blog.com/post?id=1&content=<details open ontoggle=alert(1)>',
            'http://app.com/profile?name=<body onload=alert("Hacked")>',
            'http://shop.com/search?query=<a href="javascript:alert(1)">Click Me</a>',
            'http://site.com/feedback?data=<math><mtext><option><fake><script>alert(1)</script>',
            'http://test.com/user?id=<input onfocus=alert(1) autofocus>',
            'http://app.com/v1/data?val=<video><source onerror=alert(1)>',

            # --- PATH TRAVERSAL / DIRECTORY TRAVERSAL ---
            'http://evil.com/../../../etc/passwd',
            'http://test.com/download?file=../../windows/win.ini',
            'http://docs.com/view/..%2f..%2f..%2fetc%2fpasswd',
            'http://site.com/img?name=..\\..\\..\\windows\\system32\\config\\sam',
            'http://app.com/files?path=%2e%2e%2f%2e%2e%2f%2e%2e%2fetc/shadow',
            'http://test.com/load?url=file:///etc/passwd',
            'http://site.com/read?file=....//....//....//etc/group',
            'http://app.com/get?data=..%c0%af..%c0%af..%c0%afetc/passwd',
            'http://test.com/viewer?path=..%252f..%252f..%252fetc/passwd',

            # --- COMMAND INJECTION ---
            'http://site.com/ping?ip=127.0.0.1; ls',
            'http://app.com/exec?cmd=whoami',
            'http://test.com/run?script=ping 8.8.8.8 && cat /etc/passwd',
            'http://site.com/admin?task=check|id',
            'http://app.com/utils?cmd=`rm -rf /`',
            'http://test.com/api?action=download & type /etc/issue',
            'http://site.com/tools?name=ping -c 1 127.0.0.1 || uname -a',
            'http://app.com/system?op=$(id)',
        ],
        'label': [
            # 40 Safe URLs
            'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe',
            'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe',
            'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe',
            'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe', 'Safe',

            # 12 SQL Injection
            'Malicious', 'Malicious', 'Malicious', 'Malicious', 'Malicious', 'Malicious',
            'Malicious', 'Malicious', 'Malicious', 'Malicious', 'Malicious', 'Malicious',

            # 11 XSS
            'Malicious', 'Malicious', 'Malicious', 'Malicious', 'Malicious', 'Malicious',
            'Malicious', 'Malicious', 'Malicious', 'Malicious', 'Malicious',

            # 9 Path Traversal
            'Malicious', 'Malicious', 'Malicious', 'Malicious', 'Malicious',
            'Malicious', 'Malicious', 'Malicious', 'Malicious',

            # 8 Command Injection
            'Malicious', 'Malicious', 'Malicious', 'Malicious',
            'Malicious', 'Malicious', 'Malicious', 'Malicious'
        ],
        'attack_type': [
            # 40 None
            'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None',
            'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None',
            'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None',
            'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None',

            # 12 SQL Injection
            'SQL Injection', 'SQL Injection', 'SQL Injection', 'SQL Injection', 'SQL Injection', 'SQL Injection',
            'SQL Injection', 'SQL Injection', 'SQL Injection', 'SQL Injection', 'SQL Injection', 'SQL Injection',

            # 11 XSS
            'XSS', 'XSS', 'XSS', 'XSS', 'XSS', 'XSS', 'XSS', 'XSS', 'XSS', 'XSS', 'XSS',

            # 9 Path Traversal
            'Path Traversal', 'Path Traversal', 'Path Traversal', 'Path Traversal', 'Path Traversal',
            'Path Traversal', 'Path Traversal', 'Path Traversal', 'Path Traversal',

            # 8 Command Injection
            'Command Injection', 'Command Injection', 'Command Injection', 'Command Injection',
            'Command Injection', 'Command Injection', 'Command Injection', 'Command Injection'
        ]
    }

    df = pd.DataFrame(data)

    print("Training vectorizer...")
    # Basic feature extraction (TF-IDF on characters to capture syntax like <script>, ../ etc.)
    vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1, 3))
    X = vectorizer.fit_transform(df['url'])
    y_label = df['label']
    y_type = df['attack_type']

    print("Training classifiers...")
    # Train label classifier (Safe vs Malicious)
    clf_label = LogisticRegression(max_iter=1000)
    clf_label.fit(X, y_label)

    # Train attack type classifier
    clf_type = LogisticRegression(max_iter=1000)
    clf_type.fit(X, y_type)

    print("Saving models...")
    os.makedirs('model', exist_ok=True)
    pickle.dump(vectorizer, open('model/vectorizer.pkl', 'wb'))
    pickle.dump(clf_label, open('model/url_model.pkl', 'wb'))
    pickle.dump(clf_type, open('model/type_model.pkl', 'wb'))
    
    print("Models trained and saved successfully in the 'model' directory.")

if __name__ == '__main__':
    create_model()

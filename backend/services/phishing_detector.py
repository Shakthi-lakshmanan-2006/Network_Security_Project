import re
from utils.logger import logger

class PhishingDetector:
    
    def __init__(self):
        self.phishing_keywords = [
            'verify account', 'confirm identity', 'urgent action',
            'suspended account', 'unusual activity', 'click here immediately',
            'your account will be closed', 'confirm your information',
            'security alert', 'unauthorized access', 'verify your identity',
            'update your information', 'claim your prize', 'you have won'
        ]
        
        self.suspicious_domains = [
            'tk', 'ml', 'ga', 'cf', 'gq',  # Free TLDs often used in phishing
        ]
    
    def analyze_email(self, sender, subject, body):
        """Analyze email for phishing indicators"""
        score = 0
        indicators = []
        
        # Extract URLs from body
        urls_found = re.findall(
            r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',
            body
        )
        
        # Rule 1: Sender domain analysis
        sender_lower = sender.lower()
        if any(domain in sender_lower for domain in ['@gmail', '@yahoo', '@hotmail', '@outlook']):
            if any(keyword in sender_lower for keyword in ['admin', 'support', 'security', 'noreply']):
                score += 30
                indicators.append('Suspicious sender: Free email provider with official-sounding name')
        
        # Rule 2: Subject urgency
        subject_lower = subject.lower()
        urgency_keywords = ['urgent', 'immediate', 'action required', 'suspended', 'expires', 'limited time']
        if any(keyword in subject_lower for keyword in urgency_keywords):
            score += 20
            indicators.append('Urgency tactics in subject line')
        
        # Rule 3: Body keyword analysis
        body_lower = body.lower()
        matched_keywords = [kw for kw in self.phishing_keywords if kw in body_lower]
        if matched_keywords:
            score += len(matched_keywords) * 12
            indicators.append(f"Phishing keywords found: {', '.join(matched_keywords[:3])}")
        
        # Rule 4: URL analysis
        malicious_urls = []
        for url in urls_found:
            url_lower = url.lower()
            
            # Check for IP addresses in URL
            if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url):
                score += 25
                indicators.append('URL contains IP address instead of domain')
                malicious_urls.append(url)
            
            # Check for suspicious TLDs
            elif any(url_lower.endswith(f'.{tld}') for tld in self.suspicious_domains):
                score += 20
                indicators.append('URL uses suspicious free TLD')
                malicious_urls.append(url)
            
            # Check for overly long or obfuscated URLs
            elif len(url) > 75 or url.count('-') > 3:
                score += 15
                indicators.append('URL appears obfuscated or abnormally long')
                malicious_urls.append(url)
        
        # Rule 5: Spelling and grammar (basic check)
        common_misspellings = ['paypal', 'microsoft', 'amazon', 'google', 'apple']
        for word in common_misspellings:
            # Check for variations like "Paypa1", "Micros0ft"
            if re.search(f'{word[:-1]}[0-9]', body_lower):
                score += 25
                indicators.append(f'Possible brand impersonation: {word}')
                break
        
        # Cap score at 100
        score = min(score, 100)
        
        return {
            'threat_score': score,
            'flagged': score >= 50,
            'indicators': indicators,
            'urls_found': urls_found,
            'malicious_urls': malicious_urls
        }
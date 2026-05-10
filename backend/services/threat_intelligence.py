import requests
from config import Config
from utils.logger import logger
import random

class ThreatIntelligenceService:
    
    @staticmethod
    def check_ip_reputation(ip_address):
        """Check IP reputation using AbuseIPDB or fallback to mock data"""
        
        # If no API key, use mock data for testing
        if not Config.ABUSEIPDB_API_KEY:
            # Generate realistic mock scores
            if ip_address.startswith("192.168") or ip_address.startswith("10."):
                mock_score = random.randint(0, 20)  # Private IPs are usually safe
            else:
                mock_score = random.randint(0, 85)  # Public IPs vary
            
            return {
                'reputation_score': mock_score,
                'is_malicious': mock_score > 50,
                'country': 'Unknown',
                'isp': 'Unknown',
                'source': 'Mock Engine (No API Key Configured)'
            }
        
        try:
            url = 'https://api.abuseipdb.com/api/v2/check'
            headers = {
                'Accept': 'application/json',
                'Key': Config.ABUSEIPDB_API_KEY
            }
            params = {
                'ipAddress': ip_address,
                'maxAgeInDays': '90'
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json().get('data', {})
                score = data.get('abuseConfidenceScore', 0)
                
                return {
                    'reputation_score': score,
                    'is_malicious': score > 50,
                    'country': data.get('countryName', 'Unknown'),
                    'isp': data.get('isp', 'Unknown'),
                    'usage_type': data.get('usageType', 'Unknown'),
                    'source': 'AbuseIPDB API v2'
                }
            else:
                logger.warning(f"AbuseIPDB API returned status {response.status_code}")
                
        except Exception as e:
            logger.error(f"Threat intelligence lookup failed: {str(e)}")
        
        # Fallback
        return {
            'reputation_score': 0,
            'is_malicious': False,
            'country': 'Unknown',
            'isp': 'Unknown',
            'source': 'Default (API Error)'
        }
    
    @staticmethod
    def check_url_reputation(url):
        """Check URL reputation using VirusTotal or fallback"""
        
        if not Config.VIRUSTOTAL_API_KEY:
            # Mock URL scanning
            suspicious_keywords = ['login', 'verify', 'account', 'paypal', 'bank', 'security']
            is_suspicious = any(keyword in url.lower() for keyword in suspicious_keywords)
            
            return {
                'is_malicious': is_suspicious,
                'detections': random.randint(0, 5) if is_suspicious else 0,
                'source': 'Mock URL Scanner (No API Key)'
            }
        
        try:
            # VirusTotal URL scan endpoint
            url_endpoint = 'https://www.virustotal.com/vtapi/v2/url/report'
            params = {
                'apikey': Config.VIRUSTOTAL_API_KEY,
                'resource': url
            }
            
            response = requests.get(url_endpoint, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                positives = data.get('positives', 0)
                total = data.get('total', 0)
                
                return {
                    'is_malicious': positives > 0,
                    'detections': positives,
                    'total_scanners': total,
                    'source': 'VirusTotal API v2'
                }
                
        except Exception as e:
            logger.error(f"URL reputation check failed: {str(e)}")
        
        return {
            'is_malicious': False,
            'detections': 0,
            'source': 'Default (API Error)'
        }
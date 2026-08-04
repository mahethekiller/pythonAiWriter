"""
WordPress REST API Direct Publisher for PythonAiWriter.
Authenticates via Application Passwords and publishes posts to WordPress blogs with 1 click.
"""

import requests
from typing import Dict, Any, Optional, Tuple
from requests.auth import HTTPBasicAuth


class WordPressPublisher:
    """Client for WordPress REST API post publishing and authentication testing."""

    def __init__(self, site_url: str, username: str, app_password: str):
        # Normalize site URL
        url = site_url.strip().rstrip("/")
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        self.site_url = url
        self.username = username.strip()
        self.app_password = app_password.strip()

    def test_connection(self) -> Tuple[bool, str]:
        """Verifies API credentials against WordPress /wp-json/wp/v2/users/me endpoint."""
        endpoint = f"{self.site_url}/wp-json/wp/v2/users/me"
        try:
            res = requests.get(
                endpoint,
                auth=HTTPBasicAuth(self.username, self.app_password),
                timeout=12
            )
            if res.status_code == 200:
                user_data = res.json()
                display_name = user_data.get("name", self.username)
                return True, f"Connected successfully as '{display_name}'!"
            elif res.status_code == 401 or res.status_code == 403:
                return False, "Authentication Failed: Incorrect Username or Application Password."
            elif res.status_code == 404:
                return False, f"WordPress REST API not found at '{endpoint}'. Verify your Site URL."
            else:
                return False, f"WordPress API Error (HTTP {res.status_code}): {res.text[:200]}"
        except Exception as exc:
            return False, f"Connection Failed: {str(exc)}"

    def publish_post(
        self,
        title: str,
        content_html: str,
        meta_description: str = "",
        status: str = "draft",
        categories: Optional[list] = None,
        tags: Optional[list] = None
    ) -> Dict[str, Any]:
        """Publishes post to WordPress REST API endpoint /wp-json/wp/v2/posts."""
        endpoint = f"{self.site_url}/wp-json/wp/v2/posts"
        
        payload = {
            "title": title,
            "content": content_html,
            "status": status,  # 'draft' or 'publish'
            "excerpt": meta_description,
            "comment_status": "open"
        }

        try:
            res = requests.post(
                endpoint,
                json=payload,
                auth=HTTPBasicAuth(self.username, self.app_password),
                timeout=20
            )
            if res.status_code in [200, 201]:
                data = res.json()
                post_id = data.get("id")
                post_link = data.get("link", f"{self.site_url}/?p={post_id}")
                return {
                    "success": True,
                    "post_id": post_id,
                    "post_link": post_link,
                    "message": f"Successfully created WordPress post #{post_id} ({status.capitalize()})!"
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to publish post (HTTP {res.status_code}): {res.text[:200]}"
                }
        except Exception as exc:
            return {
                "success": False,
                "message": f"WordPress Publish Exception: {str(exc)}"
            }

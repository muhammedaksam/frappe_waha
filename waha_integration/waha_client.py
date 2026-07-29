import logging
from typing import Optional, Dict, Any, List

from waha import WahaClient

logger = logging.getLogger("waha_integration")

class WahaService:
    """Helper wrapper for WAHA HTTP API client operations."""

    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/") if base_url else ""
        self.api_key = api_key
        self.timeout = timeout
        self._client = None

    def get_client(self) -> WahaClient:
        if not self._client:
            self._client = WahaClient(base_url=self.base_url, api_key=self.api_key, timeout=self.timeout)
        return self._client

    def close(self):
        if self._client:
            try:
                self._client.close()
            except Exception as e:
                logger.warning(f"Error closing WAHA client: {e}")
            self._client = None

    # --- Session Management ---

    def list_sessions(self) -> List[Dict[str, Any]]:
        client = self.get_client()
        try:
            sessions = client.sessions.list()
            if hasattr(sessions, "dict"):
                return sessions.dict()
            return sessions if isinstance(sessions, list) else []
        except Exception as e:
            logger.error(f"WAHA list_sessions error: {e}")
            return []

    def start_session(self, session_name: str) -> Dict[str, Any]:
        client = self.get_client()
        try:
            res = client.sessions.start(session=session_name)
            return res if isinstance(res, dict) else {"status": "started", "name": session_name}
        except Exception as e:
            logger.error(f"WAHA start_session error: {e}")
            return {"error": str(e)}

    def stop_session(self, session_name: str) -> Dict[str, Any]:
        client = self.get_client()
        try:
            res = client.sessions.stop(session=session_name)
            return res if isinstance(res, dict) else {"status": "stopped", "name": session_name}
        except Exception as e:
            logger.error(f"WAHA stop_session error: {e}")
            return {"error": str(e)}

    def get_qr_code(self, session_name: str) -> Optional[str]:
        client = self.get_client()
        try:
            qr_res = client.auth.get_qr(session=session_name, params={"format": "raw"})
            if isinstance(qr_res, dict):
                return qr_res.get("qr") or qr_res.get("value")
            elif isinstance(qr_res, str):
                return qr_res
            return str(qr_res)
        except Exception as e:
            logger.error(f"WAHA get_qr_code error for session {session_name}: {e}")
            return None

    # --- Message Sending ---

    def send_text(self, session_name: str, chat_id: str, text: str, reply_to: Optional[str] = None) -> Dict[str, Any]:
        client = self.get_client()
        payload = {
            "chatId": format_chat_id(chat_id),
            "text": text,
        }
        if reply_to:
            payload["reply_to"] = reply_to

        try:
            res = client.chatting.send_text(session=session_name, payload=payload)
            return res if isinstance(res, dict) else {"status": "sent", "response": str(res)}
        except Exception as e:
            logger.error(f"WAHA send_text error to {chat_id}: {e}")
            return {"error": str(e)}

    def send_file(self, session_name: str, chat_id: str, file_url: str, caption: Optional[str] = None, filename: Optional[str] = None) -> Dict[str, Any]:
        client = self.get_client()
        payload = {
            "chatId": format_chat_id(chat_id),
            "file": {
                "url": file_url,
            }
        }
        if caption:
            payload["caption"] = caption
        if filename:
            payload["file"]["filename"] = filename

        try:
            res = client.chatting.send_file(session=session_name, payload=payload)
            return res if isinstance(res, dict) else {"status": "sent", "response": str(res)}
        except Exception as e:
            logger.error(f"WAHA send_file error to {chat_id}: {e}")
            return {"error": str(e)}

    def send_buttons(self, session_name: str, chat_id: str, title: str, buttons: List[Dict[str, str]], footer: Optional[str] = None) -> Dict[str, Any]:
        client = self.get_client()
        payload = {
            "chatId": format_chat_id(chat_id),
            "title": title,
            "buttons": buttons,
        }
        if footer:
            payload["footer"] = footer

        try:
            if hasattr(client.chatting, "send_buttons"):
                res = client.chatting.send_buttons(session=session_name, payload=payload)
                return res if isinstance(res, dict) else {"status": "sent"}
            else:
                btn_text = f"{title}\n\n" + "\n".join([f"• [{b.get('id', idx+1)}] {b.get('text')}" for idx, b in enumerate(buttons)])
                if footer:
                    btn_text += f"\n\n_{footer}_"
                return self.send_text(session_name=session_name, chat_id=chat_id, text=btn_text)
        except Exception as e:
            logger.error(f"WAHA send_buttons error: {e}")
            btn_text = f"{title}\n\n" + "\n".join([f"• {b.get('text')}" for b in buttons])
            return self.send_text(session_name=session_name, chat_id=chat_id, text=btn_text)


def format_chat_id(phone_or_chat_id: str) -> str:
    """Ensure phone number or chat ID ends with @c.us or @g.us"""
    if not phone_or_chat_id:
        return ""
    phone_or_chat_id = phone_or_chat_id.strip()
    if "@c.us" in phone_or_chat_id or "@g.us" in phone_or_chat_id:
        return phone_or_chat_id
    digits = "".join([c for c in phone_or_chat_id if c.isdigit()])
    return f"{digits}@c.us"

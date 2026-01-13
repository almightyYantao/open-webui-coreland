import logging
from typing import Optional
from base64 import b64decode
from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import unpad
from Cryptodome.Protocol.KDF import PBKDF2
import base64
from open_webui.env import SRC_LOG_LEVELS

class SsoToken:
    def __init__(self):
        self.ldap = ""
        self.timestamp = 0
        self.name = ""

TOKEN_ENCRYPT_KEY = b"1d6Ltt=r"  # 8 bytes key for DES
log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["RAG"])

def des_decrypt(encrypt_str: str, des_key: bytes) -> str:
    try:
        # 1. 解码 Base64 编码的加密字符串
        encrypted_data = base64.b64decode(encrypt_str)

        # 2. 直接使用 des_key 作为密钥和 IV，确保其长度是 8 字节
        key = des_key[:8]  # 取前8个字节作为密钥
        iv = key  # 使用相同的密钥作为 IV
        
        # 3. 创建 DES 解密对象，使用 CBC 模式
        cipher = DES.new(key, DES.MODE_CBC, iv)

        # 4. 解密数据并去除填充
        decrypted_data = unpad(cipher.decrypt(encrypted_data), DES.block_size)
        
        # 5. 将字节数据解码为 UTF-8 字符串
        return decrypted_data.decode('utf-8')

    except Exception as e:
        print(f"Error decrypting token: {e}")
        return ""

def parse_token(token: str) -> Optional[SsoToken]:
    log.info(f"token:{token}")
    if not token or token.strip() == "":
        return None

    val_str = ""
    try:
        val_str = des_decrypt(token, TOKEN_ENCRYPT_KEY)
    except Exception as e:
        log.error("getSessionUserFromCookie", exc_info=True)
        return None

    vals = val_str.split("-")
    log.info(f"val_str:{val_str}")

    # 3 param: ldap-timestamp-花名
    if len(vals) != 3:
        return None

    sso_token = SsoToken()
    sso_token.ldap = vals[0]
    sso_token.timestamp = int(vals[1])
    sso_token.name = vals[2]
    return sso_token

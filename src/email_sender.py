import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional


def send_email(config: dict, subject: str, html_content: str, to: Optional[str] = None) -> bool:
    """
    Send an HTML email via QQ Mail SMTP using SSL.

    Required config keys:
      - smtp_server: SMTP server address (default: 'smtp.qq.com')
      - smtp_port: SMTP SSL port (default: 465)
      - smtp_user: QQ邮箱账号 (如: 123456789@qq.com)
      - smtp_password: SMTP授权码/开通的独立密码；不是登录密码
      - from_email: 发件邮箱地址（通常与 smtp_user 相同）
      - sender_name: 发件人显示名称（可选）
      - to_email: 默认收件人邮箱（可选，如未提供则必须传入参数 to）
    
    Args:
      config: 邮件服务器及发件信息的配置字典。
      subject: 邮件主题
      html_content: HTML格式的邮件正文内容
      to: 收件人邮箱，可选；若未传则使用 config['to_email']。
    
    Returns:
      bool: True 表示发送成功，False 表示失败。
    """
    try:
        smtp_server = config.get("smtp_server", "smtp.qq.com")
        smtp_port = int(config.get("smtp_port", 465))
        smtp_user = config["smtp_user"]  # 必填
        smtp_password = config["smtp_password"]  # 必填：QQ邮箱的 SMTP 授权码
        from_email = config.get("from_email", smtp_user)
        sender_name = config.get("sender_name", "")

        recipient = to if to else config.get("to_email")
        if not recipient:
            logging.error("send_email: 收件人邮箱未指定（参数 to 未提供且 config 中也没有 to_email）")
            return False

        # 构建邮件消息（MIME 邮件，HTML 内容，UTF-8 编码）
        msg = MIMEMultipart("alternative")
        # From 头：包含显示名称时如 'Name <email@example.com>'
        if sender_name:
            from_header = f"{sender_name} <{from_email}>"
        else:
            from_header = from_email
        msg["From"] = from_header
        msg["To"] = recipient
        msg["Subject"] = subject

        # 将 HTML 内容作为主体添加，指定 UTF-8 编码，确保中文等字符正确显示
        html_part = MIMEText(html_content, "html", _charset="utf-8")
        msg.attach(html_part)

        # 使用 SSL 连接到 QQ 邮箱 SMTP 服务器（端口 465）并发送
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, [recipient], msg.as_string())

        logging.info("send_email: 邮件发送成功 to=%s", recipient)
        return True
    except Exception as e:
        logging.exception("send_email: 发送邮件失败: %s", e)
        return False


if __name__ == "__main__":  # 简单自检提示
    logging.basicConfig(level=logging.INFO)
    print("模块加载完成：可以通过 from email_sender import send_email 调用发送邮件功能")

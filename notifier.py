import httpx

def send_notification(webhook_url: str, text: str, title: str = None, fields: dict = None) -> bool:
    if not webhook_url:
        return False

    # Simple autodetection of the webhook provider
    is_discord = "discord.com" in webhook_url or "discordapp.com" in webhook_url

    if is_discord:
        embed = {
            "title": title or "Wallet Alert",
            "description": text,
            "color": 15548997,
        }
        if fields:
            embed["fields"] = [
                {"name": k, "value": str(v), "inline": True}
                for k, v in fields.items()
            ]
        payload = {"embeds": [embed]}
    else:
        blocks = []
        if title:
            blocks.append({
                "type": "header",
                "text": {"type": "plain_text", "text": title}
            })
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": text}
        })
        if fields:
            field_texts = [f"*{k}*:\n{v}" for k, v in fields.items()]
            # Slack limits section fields to 10 items max
            blocks.append({
                "type": "section",
                "fields": [{"type": "mrkdwn", "text": ft} for ft in field_texts[:10]]
            })
        payload = {"blocks": blocks}

    # print(f"Sending payload: {payload}")

    try:
        resp = httpx.post(webhook_url, json=payload, timeout=10.0)
        resp.raise_for_status()
        return True
    except httpx.HTTPError as e:
        # Don't let webhook failures crash the block scanner
        print(f"Notification dispatch failed: {e}")
        return False

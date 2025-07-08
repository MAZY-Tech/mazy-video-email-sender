from .config import logger
# from .database import collection
from .database import collection as get_collection
from datetime import datetime, timezone

def add_notification_history(cognito_user_id: str, recipient_email: str, video_id: str = None):
    try:
        item = {
            "cognito_user_id": cognito_user_id,
            "recipient_email": recipient_email,
            "video_id": video_id,
            "sent_at": datetime.now(timezone.utc)
        }
        logger.debug(f'Prepared item: {item}')
        db_collection = get_collection()
        result = db_collection.insert_one(item)
        logger.info(
            f"Envio de email registrado no historico com sucesso. "
            f"History ID: {result.inserted_id}"
        )

    except Exception:
        logger.exception(f"Falha ao salvar historico")
        raise
import time

import db
import utils


def genOutsideCode(session, callbackURI):
    """Generate a new outside code"""
    with db.db_session:
        code = utils.genRandHash()
        expired = int(time.time()) + 60 * 10  # 10 minutes

        db.OutsideVerifyCode(
            code=code, session=session, expired=expired, callbackURI=callbackURI
        )

        return code


def genInsideCode(session):
    """Generate a new inside code"""
    with db.db_session:
        code = utils.genRandHash()
        expired = int(time.time()) + 60 * 1  # 1 minutes

        db.InsideVerifyCode(code=code, session=session, expired=expired)

        return code


def verifyOutsideCode(code):
    """Verify the outside code"""
    with db.db_session:
        result = db.OutsideVerifyCode.get(code=code)

        # [Check]: If code is valid
        if result is None:
            return None

        result = result.to_dict()
        db.OutsideVerifyCode[code].delete()

        # [Check]: If code is expired
        if result["expired"] < time.time():
            return None

        return result


def verifyInsideCode(code):
    """Verify the inside code"""
    with db.db_session:
        result = db.InsideVerifyCode.get(code=code)

        # [Check]: If code is valid
        if result is None:
            return None

        result = result.to_dict()
        db.InsideVerifyCode[code].delete()

        # [Check]: If code is expired
        if result["expired"] < time.time():
            return None

        return result

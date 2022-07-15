import os

import requests
from fastapi import HTTPException

from app.logger import create_logger

TRANSACTIONS_URL = os.environ["TRANSACTIONS_URL"]
logger = create_logger()


async def createWallet():
    """Create wallet for a user
    $ http POST http://localhost:3000/wallet
    HTTP/1.1 200 OK
    Connection: keep-alive
    Date: Sun, 08 Aug 2021 19:26:53 GMT
    Keep-Alive: timeout=5
    content-length: 145
    content-type: application/json; charset=utf-8

    {
        "address": "0x7E039A00fFFD8d8C898e77e52351c799C99D3a2D",
        "id": 1,
        "privateKey": "0x67bb00f89f7b50f9e2924e423d00889c627b9acdc20b738ce00ccdcf6e4b8da0",
        "publicKey": "0x04a5a8767017f752cd2f84c97253283c742a568d4502f5a5dd89504bf9343cdb89dd"
    }
    """

    walletCreationRequest = requests.post('{}/{}'.format(TRANSACTIONS_URL, 'wallet'))
    if walletCreationRequest.status_code != 200:
        raise HTTPException(
            status_code=walletCreationRequest.status_code,
            detail="Error creating wallet",
        )

    return walletCreationRequest


async def deposit(privateKey, amount):
    """Make a payment to a wallet
    $ http POST http://localhost:5000/deposit privateKey=1 amountInEthers='0.01'
    HTTP/1.1 200 OK
    Connection: keep-alive
    Date: Sun, 08 Aug 2021 19:27:38 GMT
    Keep-Alive: timeout=5
    content-length: 538
    content-type: application/json; charset=utf-8

    {
        "chainId": 4,
        "data": "0xd0e30db0",
        "from": "0x7E039A00fFFD8d8C898e77e52351c799C99D3a2D",
        "gasLimit": {
            "hex": "0xb044",
            "type": "BigNumber"
        },
        "gasPrice": {
            "hex": "0x3b9aca08",
            "type": "BigNumber"
        },
        "hash": "0x9f98447de34d3245ce1976956334336a6302befc4f204ac44a7cac0526caa82d",
        "nonce": 0,
        "r": "0xc78a2f0914988bb37e62c16ffb91ae0335d39fd3dc246fd0c269dbaf0b331589",
        "s": "0x423f245bcc46c872404b43c34fcb789cb0d3befdd44ec928b96bb25a5a887762",
        "to": "0x76b8DA0BB9b9981403586A574d10fA783f08Aa05",
        "type": null,
        "v": 44,
        "value": {
            "hex": "0x2386f26fc10000",
            "type": "BigNumber"
        }
    }
    """
    # $ http POST http://localhost:5000/deposit privateKey=1 amountInEthers='0.01'
    BODY = {'privateKey': privateKey, 'amountInEthers': "{0:.18f}".format(amount)}
    HEADERS = {
        "content-type": "application/json",
    }

    paymentRequest = requests.post(
        '{}/{}'.format(TRANSACTIONS_URL, 'deposit'),
        json=BODY,
        headers=HEADERS,
    )
    if paymentRequest.status_code != 200:
        raise HTTPException(
            status_code=paymentRequest.status_code,
            detail="Error procesing payment",
        )
    return paymentRequest


def rechargeAWallet(privateKey, amount):
    """Recharge wallet with ethers
    $ http POST http://localhost:5000/sendPayment privateKey=0x248c amountInEthers='0.0000000000000001'
    HTTP/1.1 200 OK
    Connection: keep-alive
    Date: Wed, 13 Jul 2022 01:19:39 GMT
    content-length: 528
    content-type: application/json; charset=utf-8

    {
        "chainId": 42,
        "data": "0xd0e30db0",
        "from": "0x1735c715ae114d5A26fa8f9c05c3A95340a20a41",
        "gasLimit": {
            "hex": "0x6d78",
            "type": "BigNumber"
        },
        "gasPrice": {
            "hex": "0x9502f907",
            "type": "BigNumber"
        },
        "hash": "0x9ede78fbfde3",
        "nonce": 2,
        "r": "0x4888c320a2947269edd15a7",
        "s": "0x72ca63f2418a16b2e805c986e0",
        "to": "0x248c",
        "type": null,
        "v": 120,
        "value": {
            "hex": "0x64",
            "type": "BigNumber"
        }
    }
    """
    # $ http POST http://localhost:5000/sendPayment privateKey=0x248c amountInEthers='0.0000000000000001'
    logger.debug("--------- privateKey: %s ----------", privateKey)

    BODY = {'privateKey': privateKey, 'amountInEthers': "{0:.18f}".format(amount)}
    HEADERS = {
        "content-type": "application/json",
    }

    paymentRequest = requests.post(
        '{}/{}'.format(TRANSACTIONS_URL, 'sendPayment'),
        json=BODY,
        headers=HEADERS,
    )
    if paymentRequest.status_code != 200:
        logger.debug(" ---- paymentRequest.text----- %s", paymentRequest.text)
        # print(paymentRequest.json())
        raise HTTPException(
            status_code=paymentRequest.status_code,
            detail="Error procesing payment",
        )
    return paymentRequest

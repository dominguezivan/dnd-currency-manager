from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.schemas import party_schema, characters_schema
from app.utils.utils import *
from app.utils.transactions import *

router = APIRouter(
    prefix="/character-transaction",
    tags=["character transactions"]
)


@router.get("/getFounds/{id}", response_model=Money)
async def check_founds(id: int, db: Session = Depends(get_db)):
    await check_character_id_exists(db, id)

    copper = get_money_in_character_wallet(db, id)
    money_simplified = convert_to_simplified(copper)
    return Money(**money_simplified)


@router.get("/getFoundsInCurrency/{id}/{currency_type}", response_model=Money)
async def get_founds_simplified_to_currency_type(id: int, currency_type: str, db: Session = Depends(get_db)):
    await check_character_id_exists(db, id)
    check_currency_type(currency_type)

    money_in_copper = get_money_in_character_wallet(db, id)
    money_simplified_to_curr_type = converto_to_type(money_in_copper, currency_type)
    return Money(**money_simplified_to_curr_type)


# error when making this a get requests because of the request body
# @router.post("/checkFounds/{id}")
# async def check_founds(id: int, amount: Money, db: Session = Depends(get_db)):
#     await check_character_id_exists(db, id)
#
#     copper_amount = convert_to_copper(amount)
#     return character_has_founds(db, id, copper_amount)


@router.put("/sum/{id}/", status_code=status.HTTP_200_OK)
async def sum_money_to_character(id: int, amount: Money, db: Session = Depends(get_db)):
    await check_character_id_exists(db, id)

    copper_amount = convert_to_copper(amount)
    add_money(db, id, copper_amount)
    return {"message": "Character " + get_character_name(db, id)
                       + " (with id " + str(id) + ") has received " + str(amount)}


@router.put("/subtract/{id}/", status_code=status.HTTP_200_OK)
async def subtract_money_to_character(id: int, amount: Money, db: Session = Depends(get_db)):
    await check_character_id_exists(db, id)

    copper_amount = convert_to_copper(amount)
    subtract_money(db, id, copper_amount)
    return {"message": "Character " + get_character_name(db, id)
                       + " (with id " + str(id) + ") has lost " + str(amount)}


@router.put("/transfer/{remitter_id}/{beneficiary_id}", status_code=status.HTTP_200_OK)
async def transfer_money(remitter_id: int, amount: Money, beneficiary_id: int, db: Session = Depends(get_db)):
    await check_character_id_exists(db, remitter_id)
    await check_character_id_exists(db, beneficiary_id)

    copper_amount = convert_to_copper(amount)
    check_character_has_founds(db, remitter_id, copper_amount)
    subtract_money(db, remitter_id, copper_amount)
    add_money(db, beneficiary_id, copper_amount)
    return {"message": "Transfer completed"}
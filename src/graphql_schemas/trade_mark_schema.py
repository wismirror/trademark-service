from datetime import datetime, date
from typing import Optional

import strawberry
from strawberry.types import Info

from src.core.utils import create_subclasses_in_dict


@strawberry.type
class Query:

    @strawberry.field
    async def trade_mark(self, info: Info, trade_mark_name: str) -> Optional['TradeMarkData']:
        trade_mark_data = await info.context['database'].find_trade_mark(trade_mark_name=trade_mark_name)
        result = TradeMarkData(**create_subclasses_in_dict(module_name=__name__, data=trade_mark_data))
        return result

    @strawberry.field
    async def trade_mark_similarity(self, info: Info, trade_mark_name: str
                                    , limit: int = None) -> list[Optional['TradeMarkDataWithSimilarity']]:
        nearest_trade_marks_data = await info.context['database'].find_nearest_trade_marks(
            trade_mark_name=trade_mark_name,
            limit=limit
        )
        result = [
            TradeMarkDataWithSimilarity(**create_subclasses_in_dict(module_name=__name__, data=trade_mark_data))
            for trade_mark_data in nearest_trade_marks_data
        ]
        return result


@strawberry.type
class TradeMarkDataWithSimilarity:
    _id: str
    score: str
    xmlns: Optional[str] = None
    xmlnsxsi: Optional[str] = None
    xsischemaLocation: Optional[str] = None
    TradeMarkTransactionBody: Optional['TradeMarkTransactionBody'] = None
    TransactionHeader: Optional['TransactionHeader'] = None


@strawberry.type
class TradeMarkData:
    _id: str
    xmlns: Optional[str] = None
    xmlnsxsi: Optional[str] = None
    xsischemaLocation: Optional[str] = None
    TradeMarkTransactionBody: Optional['TradeMarkTransactionBody'] = None
    TransactionHeader: Optional['TransactionHeader'] = None


@strawberry.type
class TradeMarkTransactionBody:
    TransactionContentDetails: Optional['TransactionContentDetails'] = None


@strawberry.type
class TransactionContentDetails:
    TransactionIdentifier: Optional[str] = None
    TransactionCode: Optional[str] = None
    TransactionData: Optional['TransactionData'] = None


@strawberry.type
class TransactionData:
    TradeMarkDetails: Optional['TradeMarkDetails'] = None


@strawberry.type
class TradeMarkDetails:
    TradeMark: Optional['TradeMark'] = None


@strawberry.type
class TradeMark:
    operationCode: Optional[str] = None
    RegistrationOfficeCode: Optional[str] = None
    ApplicationNumber: Optional[str] = None
    ApplicationDate: Optional[str] = None
    RegistrationDate: Optional[str] = None
    ApplicationLanguageCode: Optional[str] = None
    SecondLanguageCode: Optional[str] = None
    ExpiryDate: Optional[str] = None
    MarkCurrentStatusCode: Optional['MarkCurrentStatusCode'] = None
    MarkCurrentStatusDate: Optional[date] = None
    KindMark: Optional[str] = None
    MarkFeature: Optional[str] = None
    TradeDistinctivenessIndicator: Optional[str] = None
    WordMarkSpecification: Optional['WordMarkSpecification'] = None
    GoodsServicesDetails: Optional['GoodsServicesDetails'] = None
    PriorityDetails: Optional['PriorityDetails'] = None
    PublicationDetails: Optional['PublicationDetails'] = None
    ApplicantDetails: Optional['ApplicantDetails'] = None
    RepresentativeDetails: Optional['RepresentativeDetails'] = None


@strawberry.type
class MarkCurrentStatusCode:
    milestone: Optional[str] = None
    status: Optional[str] = None
    text: Optional[str] = None


@strawberry.type
class WordMarkSpecification:
    MarkVerbalElementText: Optional[str] = None


@strawberry.type
class GoodsServicesDetails:
    GoodsServices: Optional['GoodsServices'] = None


@strawberry.type
class GoodsServices:
    ClassificationVersion: Optional[Optional[str]] = None
    ClassDescriptionDetails: Optional['ClassDescriptionDetails'] = None


@strawberry.type
class ClassDescriptionDetails:
    ClassDescription: Optional['ClassDescription'] = None


@strawberry.type
class ClassDescription:
    ClassNumber: Optional[str] = None
    GoodsServicesDescription: Optional[list['GoodsServicesDescription']] = None


@strawberry.type
class GoodsServicesDescription:
    languageCode: Optional[str] = None
    text: Optional[str] = None


@strawberry.type
class PriorityDetails:
    Priority: Optional['Priority'] = None


@strawberry.type
class Priority:
    PriorityCountryCode: Optional[str] = None
    PriorityNumber: Optional[str] = None
    PriorityDate: Optional[date] = None
    PriorityPartialIndicator: Optional[str] = None
    PriorityStatusCode: Optional[str] = None


@strawberry.type
class PublicationDetails:
    Publication: Optional[list['Publication']] = None


@strawberry.type
class Publication:
    PublicationIdentifier: Optional[str] = None
    PublicationSection: Optional[str] = None
    PublicationDate: Optional[date] = None
    PublicationPage: Optional[str] = None


@strawberry.type
class ApplicantDetails:
    ApplicantKey: Optional['ApplicantKey'] = None


@strawberry.type
class ApplicantKey:
    Identifier: Optional[str] = None


@strawberry.type
class RepresentativeDetails:
    RepresentativeKey: Optional['RepresentativeKey'] = None


@strawberry.type
class RepresentativeKey:
    Identifier: Optional[str] = None


@strawberry.type
class TransactionHeader:
    SenderDetails: Optional['SenderDetails'] = None


@strawberry.type
class SenderDetails:
    RequestProducerDateTime: Optional[datetime] = None

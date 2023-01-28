# pylint: disable=unused-argument
from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Dict, List, Type

# from portfolio.adapters.msa_proxy import AbstractMsaProxy
# from portfolio.domain import commands, events, model

if TYPE_CHECKING:
    from ticker.service_layer import unit_of_work


# def create_pf_sequences(
#     cmd: commands.CreatePortfolioSequences,
#     msa_proxy: AbstractMsaProxy,
#     uow: unit_of_work.AbstractUnitOfWork,
# ):
#     for pf_group in cmd.product_group_ids:
#         params = {
#             "product_group_id": pf_group["product_group_id"],
#             "start_date": cmd.start_date,
#             "end_date": cmd.end_date,
#         }
#         msa_proxy.create_pf_sequences(**params)
#         uow.handle(events.PortfolioProductCreated(**params))
#
#
# def save_pf_sequences_by_pf_product_group(
#     event: events.PortfolioProductCreated,
#     uow: unit_of_work.AbstractUnitOfWork,
#     msa_proxy: AbstractMsaProxy,
# ):
#     product_group_id = event.product_group_id
#     with uow:
#         pf_seqs = msa_proxy.get_pf_sequences_latest(product_group_id)
#         for pf_seq in pf_seqs:
#             port_type = uow.portfolio.get_portfolio_product(pf_seq.port_type)
#             if port_type is None:
#                 product_group = model.PortfolioProduct.create_from_pf_sequence(
#                     product_group_id, pf_seq
#                 )
#                 uow.portfolio.add(product_group)
#
#             # OMS에서 포폴 조회 시 port_date__lte로 마지막 일자를 가져온다.
#             uow.portfolio.add(pf_seq)
#         uow.commit()
#

EVENT_HANDLERS = {}
COMMAND_HANDLERS = {}

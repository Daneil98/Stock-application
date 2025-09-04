#include <pybind11/pybind11.h>
#include <string>
#include <iostream>
#include <transactions.hpp>

namespace py = pybind11;
using namespace std;

PYBIND11_MODULE(trading_cpp, m) {
    m.doc() = "Trading and Wallet Transactions module implemented in C++";

    // WalletTransaction
    py::class_<WalletTransaction>(m, "WalletTransaction")
        .def(py::init<double, double>(), py::arg("balance")=0.0, py::arg("stock_eq")=0.0)
        .def("buy_stock_eq_update", &WalletTransaction::buy_stock_eq_update)
        .def("sell_stock_eq_update", &WalletTransaction::sell_stock_eq_update)
        .def("buy_balance_update", &WalletTransaction::buy_balance_update)
        .def("sell_balance_update", &WalletTransaction::sell_balance_update);

    // StockHolding
    py::class_<StockHolding, WalletTransaction>(m, "StockHolding")
        .def(py::init<double, double>())
        .def("buy_shares", &StockHolding::buy_shares)
        .def("sell_shares", &StockHolding::sell_shares);

    // BuyTransaction
    py::class_<BuyTransaction>(m, "BuyTransaction")
        .def(py::init<double, double>(), py::arg("balance")=0.0, py::arg("shares")=0.0)
        .def("share_number", &BuyTransaction::share_number)
        .def("charge", &BuyTransaction::charge);

    // SellTransaction
    py::class_<SellTransaction>(m, "SellTransaction")
        .def(py::init<double, double>(), py::arg("balance")=0.0, py::arg("shares")=0.0)
        .def("share_number", &SellTransaction::share_number)
        .def("sell", &SellTransaction::sell);

    // Trading
    py::class_<Trading>(m, "Trading")
        .def(py::init<double, int>(), py::arg("balance")=0.0, py::arg("leverage")=0)
        .def("calculateLongReturn", &Trading::calculateLongReturn)
        .def("calculateShortReturn", &Trading::calculateShortReturn)
        .def("CloseTrade", &Trading::CloseTrade);
}

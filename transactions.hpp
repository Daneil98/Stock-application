
#ifndef TRANSACTIONS_HPP
#define TRANSACTIONS_HPP

#include <string>
#include <iostream>
using namespace std;
#include <iomanip>


class WalletTransaction{
    private:
        double balance, stock_eq;
    
    public:
        // Constructor to initialize values
        WalletTransaction(double bal = 0.0, double stock = 0.0) 
            : balance(bal), stock_eq(stock) {}

        // Method to update stock_eq after buying
        double buy_stock_eq_update(double total_amount){
            stock_eq += total_amount;
            return stock_eq;
        }

        // Method to update stock_eq after selling
        double sell_stock_eq_update(double total_amount){
            stock_eq -= total_amount;
        }
        // Method to update the wallet balance after buying
        double buy_balance_update(double total_amount){
            balance -= total_amount;
            return balance;
        }

        // Method to update the wallet balance after selling
        double sell_balance_update(double total_amount){
            balance += total_amount;
            return balance;
        }
};


class StockHolding: public WalletTransaction{
    private:
        string ticker;

    public:
        StockHolding(double balance, double stock_eq) 
            : WalletTransaction(balance, stock_eq) {}

        double buy_shares(double shares, double bought_shares){
            shares += bought_shares;
            return shares;
        }

        double sell_shares(double shares, double sold_shares){
            shares -= sold_shares;
            return shares;
        }
};


class BuyTransaction{
    private:
        double balance; 
        double shares;

    public:
        //Initializer
        BuyTransaction(double bal = 0.0, double shares = 0.0)
            : balance(bal), shares(shares) {}
        
        double share_number(double total_purchase_price, double price){
            double share_numbers = total_purchase_price / price;
            shares += share_numbers;
            return shares;
        }

        double charge(double amount, double shares){
            if (amount > balance){
                cout << "Insufficient funds";
                return NULL;
            }
            else{
                balance -= (amount * shares);
                return balance;
            }
        }
};


class SellTransaction{
    private:
        double balance;
        double shares;
    
    public:
        SellTransaction(double bal = 0.0, double shares = 0.0)
            : balance(bal), shares(shares) {}

        //Calculates the number of shares to be sold
        double share_number(double sell_amount, double price){
            double share_numbers = sell_amount / price;

            if (share_numbers < 0.1){
                cerr << "Transaction size is too small";
                return NULL;
            }
            else{
                return share_numbers;
            }
        }

        //Carries out the sale
        double sell(double sell_amount, double equity){
            if (sell_amount > equity){
                cerr << "You do not have enough stock equity";
                return NULL;
            }
            else{
                equity -= sell_amount;
                return equity;
            }
        }
};


class Trading{
    private:
        double balance;
        int leverage;
    
    public:
        Trading(double bal = 0.0, int leverage = 0)
            : balance(bal), leverage(leverage) {}

        double calculateLongReturn(double amount, double long_price, double current_price){
            if ((long_price <=0) || (current_price <= 0)){
                cerr << "Error: Prices must be greater than 0" << endl;
                return NULL;
            }

            if (amount <= 0){
                cerr << "Error: Amount must be greater than 0" << endl;
                return NULL;  
            }

            double spread = (current_price - long_price) / long_price;
            double returns = spread * leverage * amount;
            return returns;
        }

        double calculateShortReturn(double amount, double short_price, double current_price){
            if ((short_price <=0) || (current_price <=0)){
                cerr << "Error: Prices must be greater than 0" << endl;
                return NULL;
            }

            if (amount <= 0){
                cerr << "Error: Amount must be greater than 0" << endl;
                return NULL;  
            }

            double spread = (short_price - current_price) / short_price;
            double returns = spread * leverage * amount;
            return returns;
        }

        double CloseTrade(double returns){
            balance += returns;
            return balance;
        }
};

#endif
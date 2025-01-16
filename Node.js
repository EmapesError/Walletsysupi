const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const Cashfree = require('cashfree-sdk'); // Use the official Cashfree SDK

const app = express();
app.use(bodyParser.json());
app.use(cors());

// Cashfree API credentials
const CASHFREE_APP_ID = '805651d1a917471429d9005d30156508';
const CASHFREE_SECRET_KEY = 'cfsk_ma_prod_59f4e8c983ea3865a5a79aa9fe7340fd_42903b0e';

Cashfree.init({
    mode: 'PROD', // or 'TEST'
    appId: CASHFREE_APP_ID,
    secretKey: CASHFREE_SECRET_KEY,
});

app.post('/initiate-payment', (req, res) => {
    const { amount } = req.body;

    if (!amount || amount <= 0) {
        return res.status(400).json({ success: false, message: 'Invalid amount' });
    }

    // Create a payment order
    const orderId = `ORDER_${Date.now()}`;
    const paymentData = {
        orderId,
        orderAmount: amount,
        orderCurrency: 'INR',
        customerName: 'John Doe',
        customerEmail: 'johndoe@example.com',
        customerPhone: '9876543210',
        returnUrl: 'http://localhost:3000/payment-success',
        notifyUrl: 'http://localhost:3000/webhook',
    };

    Cashfree.payment
        .createOrder(paymentData)
        .then((response) => {
            if (response.status === 'OK') {
                res.json({ success: true, paymentLink: response.paymentLink });
            } else {
                res.status(500).json({ success: false, message: 'Payment failed' });
            }
        })
        .catch((error) => {
            console.error(error);
            res.status(500).json({ success: false, message: 'An error occurred' });
        });
});

app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});

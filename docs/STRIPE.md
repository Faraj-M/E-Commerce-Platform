# Stripe Payment Setup and Testing Guide

## Getting Your Stripe Test Keys

1. **Sign up for a free Stripe account** at https://dashboard.stripe.com/register
   - No credit card required for test mode
   - You can use test mode indefinitely

2. **Get your API keys**:
   - Go to https://dashboard.stripe.com/test/apikeys
   - You'll see two keys:
     - **Publishable key** (starts with `pk_test_`)
     - **Secret key** (starts with `sk_test_`)

3. **Add keys to your `.env` file**:
   - Create or edit `.env` in the project root directory
   - Add your keys:
     ```
     STRIPE_PUBLISHABLE_KEY=pk_test_your_actual_key_here
     STRIPE_SECRET_KEY=sk_test_your_actual_key_here
     STRIPE_WEBHOOK_SECRET=
     ```
   - **Important**: Each key must be on a single line (no line breaks)
   - **Important**: Make sure there are no spaces around the `=` sign
   - **Important**: Don't use quotes around the values
   - The webhook secret can be left empty for basic testing

4. **Restart Docker containers**:
   ```bash
   docker-compose -f infrastructure/docker-compose.yml restart web
   ```
   Or for a full restart:
   ```bash
   docker-compose -f infrastructure/docker-compose.yml down
   docker-compose -f infrastructure/docker-compose.yml up --build
   ```

## Verifying Your Keys

After restarting, you can verify your keys are loaded:
```bash
docker-compose -f infrastructure/docker-compose.yml exec web python -c "from django.conf import settings; print('Key loaded:', len(settings.STRIPE_SECRET_KEY) > 0)"
```

## Testing Payments Without Real Credit Cards

Stripe provides test mode that allows you to test payment flows without using real credit cards or money. All transactions in test mode are simulated.

### Test Card Numbers

Use these test card numbers in Stripe test mode:

**Successful Payments:**
- `4242 4242 4242 4242` - Visa (most common)
- `5555 5555 5555 4444` - Mastercard
- `3782 822463 10005` - American Express

**Use any:**
- Expiry date: Any future date (e.g., 12/25)
- CVC: Any 3 digits (e.g., 123)
- ZIP: Any 5 digits (e.g., 12345)

**Declined Cards (for testing errors):**
- `4000 0000 0000 0002` - Card declined
- `4000 0000 0000 9995` - Insufficient funds
- `4000 0000 0000 0069` - Expired card

### Testing Payment Flow

1. Add items to cart
2. Proceed to checkout
3. Fill in shipping information
4. On payment page, use test card `4242 4242 4242 4242`
5. Complete the payment - it will succeed without charging real money

### Viewing Test Transactions

All test transactions appear in your Stripe Dashboard at:
https://dashboard.stripe.com/test/payments

You can see payment status, amounts, and details without any real charges.

## Common Issues

### "Invalid API Key provided" or "Stripe API keys are not configured"
- **Check**: Make sure your `.env` file is in the project root (same level as `backend/` and `frontend/`)
- **Check**: Verify there are no extra spaces or quotes in your `.env` file
- **Check**: Make sure you copied the full key (they're long strings, ~107 characters)
- **Check**: Ensure each key is on a single line with no line breaks
- **Check**: Ensure you're using test keys (start with `pk_test_` and `sk_test_`)

### Keys not loading
- **Solution**: Make sure you restarted the containers after editing `.env`
- **Solution**: Check that the `.env` file path in `docker-compose.yml` is correct (`../.env`)
- **Solution**: Verify the file is named exactly `.env` (not `.env.txt` or similar)
- **Solution**: Try a full restart: `docker-compose -f infrastructure/docker-compose.yml down && docker-compose -f infrastructure/docker-compose.yml up --build`

### Still seeing placeholder keys
- The app will show an error if it detects placeholder keys
- Make sure you replaced the default values in your `.env` file
- Don't use the example keys from `docker-compose.yml`

## Important Notes

- **Test mode vs Live mode**: Make sure you're using test keys (start with `pk_test_` and `sk_test_`)
- **No real money**: Test mode never charges real credit cards
- **Test data only**: Test transactions don't affect your live account
- **Switch modes**: Toggle between test and live mode in Stripe Dashboard
- **Webhook secret**: Can be left empty for basic testing. Only needed for webhook verification in production.


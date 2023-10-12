# fcs-online-marketplace

- Team 21	
- harshit19044@iiitd.ac.in	
- herschelle19045@iiitd.ac.in	
- kushal19057@iiitd.ac.in	
- pragya19071@iiitd.ac.in	
- sriza20124@iiitd.ac.in	

# FCS course project


## Stripe testing

### Test cards
There are several test cards you can use for testing. Use them with any CVC, postal code, and future expiration date.

* 4242 4242 4242 4242: Succeeds and immediately processes the payment.
* 4000 0000 0000 3220: 3D Secure 2 authentication must be completed for a successful payment.
* 4000 0000 0000 9995: Always fails with a decline code of insufficient_funds.

For the full list of test cards, check Stripe's guide on https://stripe.com/docs/testing.

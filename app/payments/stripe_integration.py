import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentProcessor:
    def create_payment_intent(self, amount, vehicle_id):
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Stripe работи в стотинки
                currency='bgn',
                metadata={'vehicle_id': vehicle_id}
            )
            return intent
        except stripe.error.StripeError as e:
            return None
    
    def confirm_payment(self, payment_intent_id):
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            if intent.status == 'succeeded':
                vehicle_id = intent.metadata['vehicle_id']
                vehicle = Vehicle.objects.get(id=vehicle_id)
                vehicle.is_paid = True
                vehicle.save()
                return True
        except:
            return False
        
        return False

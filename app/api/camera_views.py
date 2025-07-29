from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Vehicle, ParkingLot
from .recognition.license_plate import LicensePlateRecognizer

class CameraEntryView(APIView):
    def post(self, request):
        camera_id = request.data.get('camera_id')
        image_data = request.data.get('image')
        
        recognizer = LicensePlateRecognizer()
        plate_number = recognizer.detect_plate(image_data)
        
        if plate_number:
            # Записване на влизането
            vehicle = Vehicle.objects.create(
                license_plate=plate_number,
                parking_lot_id=camera_id,
                entry_time=timezone.now()
            )
            
            return Response({
                'success': True,
                'plate_number': plate_number,
                'vehicle_id': vehicle.id
            })
        
        return Response({'success': False, 'error': 'Plate not detected'})

class CameraExitView(APIView):
    def post(self, request):
        plate_number = request.data.get('plate_number')
        
        try:
            vehicle = Vehicle.objects.get(
                license_plate=plate_number,
                exit_time__isnull=True
            )
            
            # Изчисляване на цената
            duration = timezone.now() - vehicle.entry_time
            hours = duration.total_seconds() / 3600
            cost = vehicle.parking_lot.hourly_rate * hours
            
            vehicle.exit_time = timezone.now()
            vehicle.total_cost = cost
            vehicle.save()
            
            return Response({
                'success': True,
                'cost': float(cost),
                'duration_hours': hours,
                'payment_required': not vehicle.is_paid
            })
            
        except Vehicle.DoesNotExist:
            return Response({'success': False, 'error': 'Vehicle not found'})

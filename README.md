# 4-1_CapstoneDesign_django

# 가상환경 설정
- $ conda env create -f capstone.yaml
- $ conda activate capstone

# 서버 실행
- $ python manage.py runserver
# 서버 실행(외부 접속 가능)
- $ python manage.py runserver 0.0.0.0:8000

# django admin
- $ python manage.py createsuperuser
- http://localhost:8000/admin/
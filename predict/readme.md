
Run: 

  docker-compose up; docker-compose down;

Build & run, if changes:

  docker-compose up --build; docker-compose down;

Run predictor:

Place images to

  docker exec -ti ic_predictor bash
  python3 /src/predict.py



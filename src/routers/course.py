from fastapi import APIRouter, Response, HTTPException
from ..models.course_model import Course
router = APIRouter(
    prefix="/course",
    tags=["course"],
)



#  sample: {
#   "has_seats": true,
#   "main_number": 4,
#   "male_seats": null,
#   "female_seats": null,
#   "name": "102暑秋高一試聽班",
#   "other_name": "試聽數學班",
#   "seats": [
#     {
#       "sn": 55154,
#       "name": "A09"
#     },
#     {
#       "sn": 55155,
#       "name": "A13"
#     },
#     {
#       "sn": 55156,
#       "name": "A15"
#     },
#     {
#       "sn": 55157,
#       "name": "B08"
#     },
#     {
#       "sn": 55158,
#       "name": "B11"
#     },
#     {
#       "sn": 55159,
#       "name": "B15"
#     },
#     {
#       "sn": 55160,
#       "name": "C11"
#     },
#     {
#       "sn": 55161,
#       "name": "D10"
#     },
#     {
#       "sn": 55162,
#       "name": "E09"
#     },
#     {
#       "sn": 55163,
#       "name": "E11"
#     },
#     {
#       "sn": 55164,
#       "name": "G09"
#     },
#     {
#       "sn": 55165,
#       "name": "G14"
#     },
#     {
#       "sn": 55166,
#       "name": "H10"
#     },
#     {
#       "sn": 55167,
#       "name": "I15"
#     },
#     {
#       "sn": 55168,
#       "name": "I13"
#     },
#     {
#       "sn": 55169,
#       "name": "A17"
#     },
#     {
#       "sn": 55170,
#       "name": "A22"
#     },
#     {
#       "sn": 55171,
#       "name": "B21"
#     },
#     {
#       "sn": 55172,
#       "name": "B23"
#     },
#     {
#       "sn": 55173,
#       "name": "B18"
#     },
#     {
#       "sn": 55174,
#       "name": "D22"
#     },
#     {
#       "sn": 55175,
#       "name": "E22"
#     },
#     {
#       "sn": 55176,
#       "name": "F18"
#     },
#     {
#       "sn": 55177,
#       "name": "F23"
#     },
#     {
#       "sn": 55178,
#       "name": "H17"
#     },
#     {
#       "sn": 55179,
#       "name": "H21"
#     },
#     {
#       "sn": 55180,
#       "name": "I20"
#     },
#     {
#       "sn": 55181,
#       "name": "I22"
#     },
#     {
#       "sn": 55182,
#       "name": "J18"
#     },
#     {
#       "sn": 55183,
#       "name": "J22"
#     }
#   ]
# }
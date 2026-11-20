from flask import render_template, request, Blueprint
import pandas as pd
import os

from app.utils.predict import predict_shortage

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/predict", methods=["POST"])
def predict():
    drug_name = request.form.get("drug_name")
    quantity = request.form.get("quantity")
    location = request.form.get("location")

    prediction = predict_shortage(drug_name, quantity, location)

    return render_template(
        "result.html",
        drug_name=drug_name,
        quantity=quantity,
        location=location,
        prediction=prediction,
    )
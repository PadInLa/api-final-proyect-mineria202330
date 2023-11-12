from flask import Flask
from flask_graphql import GraphQLView
import graphene
import joblib
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Load the pre-trained model and encoder
model_classifier = joblib.load('models/model_classification.joblib')
encoder = joblib.load('models/model_encoder.joblib')

# Define the categorical columns
categorical_columns = ['Bancarizado', 'Discapacidad', 'Etnia', 'Genero', 'NivelEscolaridad', 'CantidadDeBeneficiarios', 'TipoPoblacion', 'RangoEdad' ]

class Query(graphene.ObjectType):
    predict_benefit = graphene.Field(
        graphene.String,
        bancarizado=graphene.String(),
        discapacidad=graphene.String(),
        etnia=graphene.String(),
        nivel_escolaridad=graphene.String(),
        genero=graphene.String(),
        tipo_poblacion=graphene.String(),
        cantidad_de_beneficiarios=graphene.Int(),
        rango_edad=graphene.Float()
    )

    def resolve_predict_benefit(self, info, bancarizado, discapacidad, etnia, nivel_escolaridad, genero, tipo_poblacion, cantidad_de_beneficiarios, rango_edad):
        data = {
            'Bancarizado': [bancarizado],
            'Discapacidad': [discapacidad],
            'Etnia': [etnia],
            'NivelEscolaridad': [nivel_escolaridad],
            'Genero': [genero],
            'TipoPoblacion': [tipo_poblacion],
            'CantidadDeBeneficiarios': [cantidad_de_beneficiarios],
            'RangoEdad': [rango_edad],
        }
        sample_df = pd.DataFrame(data)
        sample_encoded = encoder.transform(sample_df[categorical_columns])
        prediction = model_classifier.predict(sample_encoded)
        return str(prediction[0])

# Define the schema
schema = graphene.Schema(query=Query)

# Add GraphQL view
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=False  # Set to False to disable the GraphiQL interface
    )
)

# Run the app
if __name__ == '__main__':
    app.run()
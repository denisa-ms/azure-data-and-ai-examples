# DESCRIPTION:
#     This example shows how to extract json data from invoices using the Form Recognizer SDK.
# USAGE:
#   Make sure to build a virtual environment and install the following packages:
#       pip install -r requirements.txt
#   Create a file in this folder called ".env" and add the following lines:
#       AZURE_FORM_RECOGNIZER_ENDPOINT = "https://<your-custom-subdomain>.cognitiveservices.azure.com/"
#       AZURE_FORM_RECOGNIZER_KEY = "<your-form-recognizer-resource-key>"
#   Run the sample with:     
#       python form_recognizer_example.py
#     
#   For more information about how to use the Form Recognizer SDK, see:
#   https://docs.microsoft.com/en-us/azure/cognitive-services/form-recognizer/quickstarts/client-library?tabs=preview%2Cv2-1&pivots=programming-language-python


import os
from dotenv import load_dotenv
import os
import json
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()
endpoint = os.environ["AZURE_FORM_RECOGNIZER_ENDPOINT"]
key = os.environ["AZURE_FORM_RECOGNIZER_KEY"]

def extract_fields(json_object, property_name, property_value):
    if property_value:
        json_object[property_name] = {}
        json_object[property_name]["value"] = property_value.value
        json_object[property_name]["confidence"] =property_value.confidence

def extract_address(json_object, property_name, property_value):
    if property_value:
        json_object[property_name] = {}
        json_object[property_name]["value"] = {}
        json_object[property_name]["value"]["city"] = property_value.value.city
        json_object[property_name]["value"]["country_region"] = property_value.value.country_region
        json_object[property_name]["value"]["house_number"] = property_value.value.house_number
        json_object[property_name]["value"]["po_box"] = property_value.value.po_box
        json_object[property_name]["value"]["postal_code"] = property_value.value.postal_code
        json_object[property_name]["value"]["road"] = property_value.value.road
        json_object[property_name]["value"]["state"] = property_value.value.state
        json_object[property_name]["value"]["street_address"] = property_value.value.street_address
        json_object[property_name]["confidence"] =property_value.confidence

def extract_date(json_object, property_name, property_value):
    if property_value:
        json_object[property_name] = {}
        json_object[property_name]["value"] = {}
        json_object[property_name]["value"]["day"] = property_value.value.day
        json_object[property_name]["value"]["month"] = property_value.value.month
        json_object[property_name]["value"]["year"] = property_value.value.year
        json_object[property_name]["confidence"] =property_value.confidence


def extract_currency(json_object, property_name, property_value):
    if property_value:
        json_object[property_name] = {}
        json_object[property_name]["value"] = {}
        json_object[property_name]["value"]["amount"] = property_value.value.amount
        json_object[property_name]["value"]["symbol"] = property_value.value.symbol
        json_object[property_name]["confidence"] =property_value.confidence



def analyze_invoices():
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    for filename in os.listdir("cognitive services/invoices/"):
        idx = 0
        with open(os.path.join("cognitive services/invoices/", filename), 'rb') as f:
            poller = document_analysis_client.begin_analyze_document(
                "prebuilt-invoice", document=f, locale="en-US"
        )   

        invoice = poller.result().documents[0]
        print("Invoice #{}".format(idx+1))
        invoice_json = {}
        invoice_json["file_name"] = filename

        extract_fields(invoice_json, "VendorName", invoice.fields.get("VendorName"))
        extract_address(invoice_json, "VendorAddress", invoice.fields.get("VendorAddress"))
        extract_fields(invoice_json, "VendorAddressRecipient", invoice.fields.get("VendorAddressRecipient"))
        extract_fields(invoice_json, "CustomerName", invoice.fields.get("CustomerName"))
        extract_fields(invoice_json, "CustomerId", invoice.fields.get("CustomerId"))
        extract_address(invoice_json, "CustomerAddress", invoice.fields.get("CustomerAddress"))
        extract_fields(invoice_json, "CustomerAddressRecipient", invoice.fields.get("CustomerAddressRecipient"))
        extract_fields(invoice_json, "InvoiceId", invoice.fields.get("InvoiceId"))
        extract_date(invoice_json, "InvoiceDate", invoice.fields.get("InvoiceDate"))
        extract_currency(invoice_json, "InvoiceTotal", invoice.fields.get("InvoiceTotal"))
        extract_date(invoice_json, "DueDate", invoice.fields.get("DueDate"))
        extract_fields(invoice_json, "PurchaseOrder", invoice.fields.get("PurchaseOrder"))
        extract_address(invoice_json, "BillingAddress", invoice.fields.get("BillingAddress"))
        extract_fields(invoice_json, "BillingAddressRecipient", invoice.fields.get("BillingAddressRecipient"))
        extract_address(invoice_json, "ShippingAddress", invoice.fields.get("ShippingAddress"))
        extract_fields(invoice_json, "ShippingAddressRecipient", invoice.fields.get("ShippingAddressRecipient"))
        invoice_json["Items"] = []  

        if (invoice.fields.get("Items")):
            for idx, item in enumerate(invoice.fields.get("Items").value):
                item_json = {}
                item = invoice.fields.get("Items").value[idx]
                extract_fields(item_json, "Name", item.value.get("Name"))
                extract_fields(item_json, "Description", item.value.get("Description"))
                extract_fields(item_json, "Quantity", item.value.get("Quantity"))
                extract_fields(item_json, "Unit", item.value.get("Unit"))
                extract_currency(item_json, "UnitPrice", item.value.get("UnitPrice"))
                extract_fields(item_json, "ProductCode", item.value.get("ProductCode"))
                extract_date(item_json, "Date", item.value.get("Date"))
                extract_currency(item_json, "Tax", item.value.get("Tax"))
                extract_currency(item_json, "Amount", item.value.get("Amount"))
                invoice_json["Items"].append(item_json)

        extract_currency(invoice_json, "SubTotal", invoice.fields.get("SubTotal"))
        extract_currency(invoice_json, "TotalTax", invoice.fields.get("TotalTax"))
        extract_currency(invoice_json, "PreviousUnpaidBalance", invoice.fields.get("PreviousUnpaidBalance"))
        extract_currency(invoice_json, "AmountDue", invoice.fields.get("AmountDue"))
        extract_date(invoice_json, "ServiceStartDate", invoice.fields.get("ServiceStartDate"))
        extract_date(invoice_json, "ServiceEndDate", invoice.fields.get("ServiceEndDate"))
        extract_date(invoice_json, "ServiceDate", invoice.fields.get("ServiceDate"))
        extract_address(invoice_json, "ServiceAddress", invoice.fields.get("ServiceAddress"))
        extract_fields(invoice_json, "ServiceAddressRecipient", invoice.fields.get("ServiceAddressRecipient"))
        extract_address(invoice_json, "RemittanceAddress", invoice.fields.get("RemittanceAddress"))
        extract_fields(invoice_json, "RemittanceAddressRecipient", invoice.fields.get("RemittanceAddressRecipient"))
        print(json.dumps(invoice_json))
        idx += 1


if __name__ == "__main__":
    analyze_invoices()
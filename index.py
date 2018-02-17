from flask_restful import Api, Resource, reqparse
from flask import Flask, request
import psycopg2

# A helper function to parse the query string
def parse_payload(string):
    d = {}
    for x in string.split("&"):
        param = x.split("=")
        d.update({param[0].strip(): param[1].strip()})
    return d


app = Flask(__name__)
api = Api(app)

########### STAGE 1 API ###################################################################################################################

class Test(Resource):
    def post(self, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument('lat', type=float, help='lat cannot be converted')
        parser.add_argument('lng', type=float, help='lng cannot be converted')
        parser.add_argument('pin', type=str, help='Rate cannot be converted')
        parser.add_argument('addr', type=str, help='Rate cannot be converted')
        parser.add_argument('cty', type=str, help='Rate cannot be converted')
        args = parser.parse_args()
        latitude = args["lat"]
        longitude = args["lng"]
        pin_code = args["pin"]
        address = args["addr"]
        city = args["cty"]
        key = 'IN/' + pin_code

        command = "select * from apitests where latitude between " + str(latitude - 0.001) + " and " + str(
            latitude + 0.001) + " and longitude between " + str(longitude - 0.001) + " and " + str(longitude + 0.001) + " or key = \'" + key + "\';"
        conn = psycopg2.connect(
            dbname="apitest", user="Priyanshu", password="pr1yanshu")
        cur = conn.cursor()
        cur.execute(command)
        rowC = cur.rowcount
        cur.close()

        if(rowC == 0):
            command1 = "insert into apitests values(" + "\'" + key + "\'" + " , " + "\'" + address + \
                "\'" + " , " + "\'" + city + "\'" + ", " + \
                str(latitude) + ", " + str(longitude) + ");"
            cur = conn.cursor()
            cur.execute(command1)
            conn.commit()
            cur.close()
            return ("Entry successfully added")
        else:
            return ("Entry aleady exists")
        print(args)
        return (args)

#################################### STAGE 2 API ##################################################################################################
class Test2(Resource):
    def get(self, **kwargs):
        query = parse_payload(kwargs["req"])
        latitude = float(query["lat"])
        longitude = float(query["lng"])
        radius = float(query["rad"])

        command = "select * from apitests where earth_box("+str(latitude)+","+str(longitude)+","+str(radius)+") @> ll_to_earth(apitests.latitude,apitests.longitude);"
        conn = psycopg2.connect(
            dbname="apitest", user="Priyanshu", password="pr1yanshu")
        cur = conn.cursor()
        cur.execute(command)
        row = cur.fetchone()
        while row is not None:
        	print(row)
        	row = cur.fetchone()
        rows = cur.fetchall()
        return(rows)
        cur.close()



class Test3(Resource):
    def get(self, **kwargs):
        query = parse_payload(kwargs["req"])
        latitude = float(query["lat"])
        latitude = latitude*0.0174533
        longitude = float(query["lng"])
        longitude = longitude*0.0174533
        radius = float(query["rad"])

        command = "SELECT * FROM apitests WHERE acos(sin("+str(latitude)+") * sin(latitude) + cos("+str(latitude)+") * cos(latitude) * cos(longitude - ("+str(longitude)+"))) * 6371 <= "+str(radius)+";"
        conn = psycopg2.connect(
            dbname="apitest", user="Priyanshu", password="pr1yanshu")
        cur = conn.cursor()
        cur.execute(command)
        row = cur.fetchone()
        while row is not None:
        	print(row)
        	row = cur.fetchone()
        rows = cur.fetchall()
        return(rows)
        cur.close()


api.add_resource(Test, '/post_location')
api.add_resource(Test2, '/get_using_postgre/<string:req>')
api.add_resource(Test3, '/get_using_self/<string:req>')
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=16000)

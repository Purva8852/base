import json
import decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


class PostsController(object):
    def __init__(self, db):
        self.table = db.Table('posts')

    def create_post(self, post_id, post_type, creator_email, source, destination, time, available_seats, total_seats):
        response = self.table.put_item(
            Item={
                'postId': post_id,
                'postType': post_type,
                'creator_email': creator_email,
                'source': source,
                'destination': destination,
                'time': time,
                'availableSeats': available_seats,
                'totalSeats': total_seats,
                'passengers': [creator_email]
            }
        )
        return response

    def get_all_posts(self):
        response = self.table.scan()
        data = json.dumps(response['Items'], cls=DecimalEncoder)
        print(data)
        return data

    def get_post_by_id(self, post_id):
        response = self.table.get_item(
            Key={
                'post_id': post_id
            }
        )
        return response['Item']

    def update_post(self, post_id, source, destination, time, available_seats, total_seats):
        response = self.table.update_item(
            Key={
                'post_id': post_id
            },
            UpdateExpression='SET source = :source, destination = :destination, time = :time, '
                             'available_seats = :available_seats, total_seats = :total_seats',
            ExpressionAttributeValues={
                ':source': source,
                ':destination': destination,
                ':time': time,
                ':available_seats': available_seats,
                ':total_seats': total_seats
            },
            ReturnValues='UPDATED_NEW'
        )
        return response

    def delete_post(self, post_id):
        response = self.table.delete_item(
            Key={
                'post_id': post_id
            }
        )
        return response
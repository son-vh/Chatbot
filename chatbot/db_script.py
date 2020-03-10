from chatbot.models import Room, BookingRoom, User

s = User(id='1')
a = Room(room_id='105B', name='105B', size=15,
         image='https://www.citizenm.com/cache/images/citizenm_rott_mtg-0156_005a44cc5a24cc.jpg',
         device='máy chiếu,ti vi,điện thoại bàn',
         type='lớn', status=1)
a.save()
b = Room(room_id='202B', name='202B', size=10,
         image=' https://www.huckletree.com/uploads/files/2018/01/09/5a54d283e6469-sla-inte-meeting-room-d2.jpg',
         device='tivi',
         type='trung bình', status=1)
b.save()
c = Room(room_id='205B', name='205B', size=16,
         image=' https://blog.go-work.com/wp-content/uploads/2018/07/Meeting-Room-South-Jakarta.jpg',
         device='điện thoại bàn',
         type='lớn', status=1)

c.save()
d = Room(room_id='106A', name='106A', size=8,
         image=' https://d2e5ushqwiltxm.cloudfront.net/wp-content/uploads/sites/20/2016/06/14135607/EVENT-3-724x357.jpg',
         device='máy chiếu,ti vi,điện thoại bàn',
         type='lớn', status=1)
d.save()
BookingRoom(room=b, user=s, date='2018-12-29', start_time='17:00:00', end_time='18:00:00', status=1,
            title='họp khách hàng', content='họp khách hàng', reason='họp khách hàng').save()

BookingRoom(room=a, user=s, date='2018-12-29', start_time='15:00:00', end_time='16:00:00', status=1,
            title='họp khách hàng', content='họp khách hàng', reason='họp khách hàng').save()

BookingRoom(room=a, user=s, date='2018-12-29', start_time='08:00:00', end_time='10:30:00', status=1,
            title='họp khách hàng', content='họp khách hàng', reason='họp khách hàng').save()

BookingRoom(room=a, user=s, date='2018-12-28', start_time='08:00:00', end_time='19:00:00', status=1,
            title='họp khách hàng', content='họp khách hàng', reason='họp khách hàng').save()

BookingRoom(room=a, user=s, date='2018-12-29', start_time='11:00:00', end_time='15:00:00', status=1,
            title='họp khách hàng', content='họp khách hàng', reason='họp khách hàng').save()

BookingRoom(room=a, user=s, date='2019-01-11', start_time='11:00:00', end_time='13:00:00', status=1,
            title='họp khách hàng', content='họp khách hàng', reason='họp khách hàng').save()

BookingRoom(room=a, user=s, date='2018-12-29', start_time='17:00:00', end_time='19:00:00', status=1,
            title='họp khách hàng', content='họp khách hàng', reason='họp khách hàng').save()

BookingRoom(room=a, user=s, date='2019-01-28', start_time='08:00:00', end_time='10:00:00', status=1,
            title='họp khách hàng', content='họp khách hàng', reason='họp khách hàng').save()

BookingRoom(room=a, user=s, date='2019-01-28', start_time='10:30:00', end_time='11:00:00', status=1,
            title='họp khách hàng', content='họp khách hàng', reason='họp khách hàng').save()

BookingRoom(room=a, user=s, date='2019-01-28', start_time='11:30:00', end_time='12:00:00', status=1,
            title='họp khách hàng', content='họp khách hàng', reason='họp khách hàng').save()
# from chatbot import db_script

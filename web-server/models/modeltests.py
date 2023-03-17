import unittest
import scene

class userManagerTest(unittest.TestCase):
    def setUp(self):
        self.user_manager = scene.UserManager()

    def test_add_user(self):
        id = "1234"
        user = scene.User('me','pass123',id)
        self.user_manager.set_user(user)


        ret=self.user_manager.get_user_by_id(id)

        print(user)
        print(ret)

        self.assertTrue(ret.username==user.username)
        self.assertTrue(ret.password==user.password)
        self.assertTrue(ret.id==user.id)




if __name__=='__main__':
    unittest.main()
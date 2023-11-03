import unittest
from dataclasses.user import User
from managers.usermanager import UserManager


class userManagerTest(unittest.TestCase):
    def setUp(self):  # fires before the test starts
        self.user_manager = UserManager()
        self.user_manager.collection.drop()

    def test_set_user(self):
        user = User('me', 'pass123', "1234")
        self.user_manager.set_user(user)

        user2 = User('Jack Ryan', 'qwerty', '12345')
        self.user_manager.set_user(user2)

        user3 = User('Jack Ryan', 'pass123', '43279')  # has same username as user2

        user4 = User('Theodore K.', 'letmein', '1234')  # has same id as user1

        ret = self.user_manager.get_user_by_id(user._id)

        print("User == " + str(user))
        print("User2 == " + str(user2))
        print("User returned from mongodb == " + str(ret))

        errorcode = self.user_manager.set_user(user3)

        exceptionRaised = False

        try:  # should raise an exception because it has the same id
            self.user_manager.set_user(user4)
        except:
            exceptionRaised = True

        self.assertTrue(exceptionRaised)

        self.assertTrue(ret.username == user.username)
        self.assertTrue(ret.password == user.password)
        self.assertTrue(ret._id == user._id)

        self.assertFalse(ret.username == user2.username)
        self.assertFalse(ret.password == user2.password)
        self.assertFalse(ret._id == user2._id)

        self.assertTrue(errorcode == 1)

    # def tearDown(self):                    #fires after the test is completed
    # self.user_manager.collection.drop()

    def test_generate_user(self):
        user1 = self.user_manager.generate_user("Jill Stingray", "password456")
        print(user1)

        ret = self.user_manager.get_user_by_username("Jill Stingray")

        self.assertTrue(user1._id == ret._id)
        self.assertTrue("Jill Stingray" == ret.username)

        # this should return 1 because the username already exists
        user2 = self.user_manager.generate_user("Jill Stingray", "doggy")

        self.assertTrue(type(user2) == int)
        self.assertTrue(user2 == 1)


if __name__ == '__main__':
    unittest.main()

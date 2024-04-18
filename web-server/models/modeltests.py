import unittest
import scene
import os
from dotenv import load_dotenv

class userManagerTest(unittest.TestCase):
    def setUp(self):                            #fires before the test starts
        print("START SETUP FOR TESTS")
        self.user_manager = scene.UserManager(True)
        self.user_manager.collection.drop()
        print("FINISHED USER TEST SETUP")

    def test_set_user(self):
        user = scene.User('me','pass123',"1234")
        self.user_manager.set_user(user)

        user2 = scene.User('Jack Ryan','qwerty','12345')
        self.user_manager.set_user(user2)

        user3 = scene.User('Jack Ryan','pass123','43279') #has same username as user2

        user4 = scene.User('Theodore K.','letmein','1234') #has same id as user1


        ret=self.user_manager.get_user_by_id(user._id)

        print("User == "+str(user))
        print("User2 == "+str(user2))
        print("User returned from mongodb == "+str(ret))

        errorcode=self.user_manager.set_user(user3)


        exceptionRaised = False

        try:  #should raise an exception because it has the same id
            self.user_manager.set_user(user4)
        except:
            exceptionRaised=True

        self.assertTrue(exceptionRaised)

        self.assertTrue(ret.username==user.username)
        self.assertTrue(ret.password==user.password)
        self.assertTrue(ret._id==user._id)

        self.assertFalse(ret.username==user2.username)
        self.assertFalse(ret.password==user2.password)
        self.assertFalse(ret._id==user2._id)

        self.assertTrue(errorcode==1)

    #def tearDown(self):                    #fires after the test is completed
        #self.user_manager.collection.drop()


    def test_generate_user(self):
        user1=self.user_manager.generate_user("Jill Stingray","password456")
        print(user1)

        ret=self.user_manager.get_user_by_username("Jill Stingray")

        self.assertTrue(user1._id==ret._id)
        self.assertTrue("Jill Stingray"==ret.username)

        user2=self.user_manager.generate_user("Jill Stingray","doggy") #this should return 1 because the username already exists

        self.assertTrue(type(user2)==int)
        self.assertTrue(user2==1)


class environmentTest(unittest.TestCase):
    def setUp(self):                            #fires before the test starts
        load_dotenv()

    def test_environment(self):
        print("Username:", os.getenv("RABBITMQ_DEFAULT_USER"))
        print("Password: ", os.getenv("MONGO_INITDB_ROOT_PASSWORD"))
        assert("admin" == os.getenv("RABBITMQ_DEFAULT_USER") == os.getenv("MONGO_INITDB_ROOT_USERNAME"))
        assert("password123" == os.getenv("RABBITMQ_DEFAULT_PASS") == os.getenv("MONGO_INITDB_ROOT_PASSWORD"))
        assert("mongodb" == os.getenv("MONGO_IP"))
        assert("rabbitmq" == os.getenv("RABBITMQ_IP"))


class queueListManagerTest(unittest.TestCase):
    def setUp(self):                            #fires before the test starts
        self.queue_manager = scene.QueueListManager(True)
        self.queue_manager.collection.drop()

    def test_queues(self):
        print("APPENDING QUEUES")
        self.queue_manager.append_queue("sfm_list","uuid1")
        self.queue_manager.append_queue("sfm_list","uuid2")
        self.queue_manager.append_queue("sfm_list","uuid5")
        self.queue_manager.append_queue("sfm_list","uuid6")

        self.queue_manager.append_queue("nerf_list","uuid3")

        self.queue_manager.append_queue("queue_list","uuid4")
        
        ret=self.queue_manager.get_queue_position("sfm_list","uuid2")
        print("uuid2 is in sfm_list position {} out of {}.".format(ret[0],ret[1]))
        self.assertTrue(ret[0] == 1 and ret[1] == 4)
        print("POPPING QUEUES")
        # Popping queue positions
        self.queue_manager.pop_queue("sfm_list")
        self.queue_manager.pop_queue("sfm_list","uuid6")
        self.queue_manager.pop_queue("queue_list")

        ret=self.queue_manager.get_queue_position("sfm_list","uuid5")
        print("uuid5 is in sfm_list position {} out of {}.".format(ret[0],ret[1]))
        self.assertTrue(ret[0] == 1 and ret[1] == 2)
        # Item not found in list
        print("TESTING QUEUE EXCEPTIONS")
        exceptionRaised = False
        try:
            self.queue_manager.get_queue_position("sfm_list","uuid6")
        except:
            exceptionRaised = True
        self.assertTrue(exceptionRaised)
        # Empty list
        exceptionRaised = False
        try:
            self.queue_manager.get_queue_position("queue_list","uuid4")
        except:
            exceptionRaised = True
        self.assertTrue(exceptionRaised)
        # Popping item not in list
        exceptionRaised = False
        try:
            self.queue_manager.pop_queue("sfm_list","uuid1")
        except:
            exceptionRaised = True
        self.assertTrue(exceptionRaised)
        print("TESTING QUEUE LENGTHS")
        # Testing queue length
        ret=self.queue_manager.get_queue_size("sfm_list")
        self.assertTrue(ret == 2)
        ret=self.queue_manager.get_queue_size("queue_list")
        self.assertTrue(ret == 0)
        print("CLEARING QUEUES")
        # Clearing queues
        self.queue_manager.pop_queue("sfm_list")
        self.queue_manager.pop_queue("sfm_list")
        self.queue_manager.pop_queue("nerf_list")
        ret=self.queue_manager.get_queue_size("sfm_list")
        self.assertTrue(ret == 0)
        ret=self.queue_manager.get_queue_size("queue_list")
        self.assertTrue(ret == 0)
        ret=self.queue_manager.get_queue_size("nerf_list")
        self.assertTrue(ret == 0)
        print("QUEUE TESTS SUCCESSFUL")

if __name__=='__main__':
    unittest.main()
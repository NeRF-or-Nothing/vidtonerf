import unittest
import scene

class userManagerTest(unittest.TestCase):
    def setUp(self):                            #fires before the test starts
        self.user_manager = scene.UserManager()
        self.user_manager.collection.drop()

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



class workerManagerTest(unittest.TestCase):
    def setUp(self):                            #fires before the test starts
        self.worker_manager = scene.WorkerManager()
        self.worker_manager.collection.drop()

    def test_set_worker(self):
        worker = scene.Worker('me','pass123',"1234")
        self.worker_manager.set_worker(worker)

        worker2 = scene.Worker('Jack Ryan','qwerty','12345')
        self.worker_manager.set_worker(worker2)

        worker3 = scene.Worker('Jack Ryan','pass123','43279') #has same username as user2

        worker4 = scene.Worker('Theodore K.','letmein','1234') #has same id as user1

        ret=self.worker_manager.get_worker_by_id(worker.id)

        print("Worker == "+str(worker))
        print("Worker2 == "+str(worker2))
        print("Worker returned from mongodb == "+str(ret))

        errorcode=self.worker_manager.set_worker(worker3)


        exceptionRaised = False

        try:  #should raise an exception because it has the same id
            self.worker_manager.set_worker(worker4)
        except:
            exceptionRaised=True

        self.assertTrue(exceptionRaised)

        self.assertTrue(ret.owner_id==worker.owner_id)
        self.assertTrue(ret.api_key==worker.api_key)
        self.assertTrue(ret.id==worker.id)
        self.assertTrue(ret.type==worker.type)
        self.assertTrue(ret.scenes_assigned==worker.scenes_assigned)

        self.assertFalse(ret.owner_id==worker2.owner_id)
        self.assertFalse(ret.api_key==worker2.api_key)
        self.assertFalse(ret.id==worker2.id)
        self.assertFalse(ret.type==worker2.type)
        self.assertFalse(ret.scenes_assigned==worker2.scenes_assigned)

        self.assertTrue(errorcode==1)

    #def tearDown(self):                    #fires after the test is completed
        #self.user_manager.collection.drop()


    def test_generate_worker(self):
        worker1=self.worker_manager.generate_worker("Jill Stingray","password456")
        print(worker1)

        ret=self.worker_manager.get_workers_by_owner("Jill Stingray")

        self.assertTrue(worker1.id==ret.id)
        self.assertTrue("Jill Stingray"==ret.owner_id)

        worker2=self.worker_manager.generate_worker("Jill Stingray","doggy") #this should return 1 because the username already exists

        self.assertTrue(type(worker2)==int)
        self.assertTrue(worker2==1)


if __name__=='__main__':
    unittest.main()
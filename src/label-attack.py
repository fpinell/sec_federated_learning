from federated_learning import Setup, Client
import random
import argparse
import logging
import numpy
import enum
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import signal
import sys
from baseliner import seven2one


# Just a 7 (n. 42 in MNIST, coincidence?)
ORIGINAL = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 26, 111, 195, 230, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 28, 107, 195, 254, 254, 254, 244, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 46, 167, 248, 254, 222, 146, 150, 254, 174, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 65, 223, 246, 254, 153, 61, 10, 0, 48, 254, 129, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 85, 175, 164, 80, 2, 0, 0, 0, 48, 254, 120, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 182, 254, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 207, 254, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 207, 202, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 28, 248, 170, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 107, 254, 61, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 166, 252, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 191, 206, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 191, 206, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 246, 186, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 91, 254, 77, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 175, 254, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 175, 240, 27, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 215, 222, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 115, 255, 152, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 134, 255, 68, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

LABEL = 0

NTRAIN = 200  # rounds of training
NTRANS = 10  # rounds for transmission tests
DELTA = 0.1
BATCH_SIZE = 32
NSELECTION = 3
FUZZMAX = 26

SCORE_LOG = 'score.csv'
EVENT_LOG = 'event.csv'

score_dict = {
        'X': [],
        'Y': []
      }
event_dict = {
        'X': [],
        'E': []
      }

def log_score(x, y):
    score_dict['X'].append(x)
    score_dict['Y'].append(y)

def log_event(x, e):
    event_dict['X'].append(x)
    event_dict['E'].append(e)


hl, = plt.plot([], [])
plt.ylim([20, 55])
plt.xlim([0,NTRAIN + (NTRANS*12)])

def update_plot(x, y):
    hl.set_xdata(numpy.append(hl.get_xdata(), [x]))
    hl.set_ydata(numpy.append(hl.get_ydata(), [y]))

def add_vline(xv):
    plt.axvline(x=xv)

def signal_handler(sig, frame):
    plt.savefig('output.png', dpi=300)
    sdf = pandas.DataFrame(score_dict)
    sdf.to_csv(SCORE_LOG)
    edf = pandas.DataFrame(event_dict)
    edf.to_csv(EVENT_LOG)
    sys.exit(0)

# compute slope through least square method
def slope(y):
    numer = 0
    denom = 0
    mean_x = (len(y) - 1)/2
    mean_y = numpy.mean(y)
    for x in range(len(y)):
        numer += (x - mean_x) * (y[x] - mean_y)
        denom += (x - mean_x) ** 2
    m = numer / denom
    return m

signal.signal(signal.SIGINT, signal_handler)

class ReceiverState(enum.Enum):
    Crafting = 1
    Calibrating = 2
    Ready = 3
    Transmitting = 4

class Sender(Client):

    def __init__(self,x_bias0,x_bias1,y_label0,y_label1,frame,replay):
        self.bit = None
        self.sent = False
        self.frame_count = -1
        self.frame = frame
        self.replay_model = replay
        x_train = numpy.array([x_bias0,x_bias1])
        y_train = numpy.array([y_label0,y_label1])
        x_train = x_train.astype('float32')
        x_train /= 255
        super().__init__("Sender",x_train, y_train, x_train, y_train)

    # Covert channel send
    def call_training(self,n_of_epoch):
        logging.debug("Sender: call_training()")
        # super().call_training(n_of_epoch)
        self.send_to_model(n_of_epoch)

    def update_model_weights(self,main_model):
        logging.debug("Sender: update_model_weights()")
        super().update_model_weights(main_model)

        logging.debug("Sender: frame_count = %s", self.frame_count)

        if self.frame_count == 0:
            pred = self.bias_prediction()
            logging.info("Sender: frame starts at %s", pred)
            self.bit = random.randint(0,1)
            logging.info("Sender: SENDING %s", self.bit)

        self.frame_count = (self.frame_count + 1) % self.frame

    def bias_prediction(self):
        x_pred = self.x_train[[1]]
        prediction = self.predict(x_pred)
        # TODO: must return max element only
        return prediction[0].index(max(prediction[0]))

    # forces biases to transmit one bit through the model
    def send_to_model(self, n_of_epoch):

            if self.bit == 1:

                logging.info("Sender: injecting bias 1")

                # bias injection dataset
                train_ds = TensorDataset(self.x_train[1:2], self.y_train[1:2])
                train_dl = DataLoader(train_ds, batch_size=BATCH_SIZE)

                # bias testing dataset
                test_ds = TensorDataset(self.x_train[1:2], self.y_train[1:2])
                test_dl = DataLoader(test_ds, batch_size=BATCH_SIZE)

                for epoch in range(n_of_epoch):

                    train_loss, train_accuracy = self.train(train_dl)
                    test_loss, test_accuracy = self.validation(test_dl)

            else:

                logging.info("Sender: injecting bias 0")

                # bias injection dataset
                train_ds = TensorDataset(self.x_train[0:1], self.y_train[0:1])
                train_dl = DataLoader(train_ds, batch_size=BATCH_SIZE)

                # bias testing dataset
                test_ds = TensorDataset(self.x_train[0:1], self.y_train[0:1])
                test_dl = DataLoader(test_ds, batch_size=BATCH_SIZE)

                for epoch in range(n_of_epoch):

                    train_loss, train_accuracy = self.train(train_dl)
                    test_loss, test_accuracy = self.validation(test_dl)

class Receiver(Client):

    def __init__(self,x_sample,y_label):
        self.bit = None
        self.selection_count = 0
        self.frame = 0
        self.m = 0
        self.x_bias1 = x_sample
        self.x_bias0 = None
        self.y_label1 = y_label
        self.y_label0 = None
        self.frame_count = 0
        self.frame_start = 0
        self.frame_end = 0
        self.state = ReceiverState.Crafting
        x_train = numpy.array([x_sample])
        y_train = numpy.array([y_label])
        x_train = x_train.astype('float32')
        x_train /= 255
        super().__init__("Receiver",x_train, y_train, x_train, y_train)

    def call_training(self,n_of_epoch):
        logging.debug("Receiver: call_training()")

        if self.state == ReceiverState.Calibrating:
            self.selection_count += 1
            logging.info("Receiver: selected %s times", self.selection_count)
            if self.selection_count > NSELECTION:
                self.state = ReceiverState.Ready
        else:
            pass

    # Covert channel receive
    def update_model_weights(self,main_model):
        logging.debug("Receiver: update_model_weights()")
        super().update_model_weights(main_model)

        logging.debug("Receiver: frame_count = %s", self.frame_count)

        if self.state == ReceiverState.Crafting:
            self.craft()
        elif self.state == ReceiverState.Calibrating:
            self.calibrate()
        else: # self.state == ReceiverState.Transmitting:
            self.read_from_model()

    def bias_prediction(self):
        x_pred = self.x_train[[1]]
        prediction = self.predict(x_pred)
        # TODO: must return max element only
        return prediction[0].index(max(prediction[0]))

    def read_from_model(self):

        pred = self.bias_prediction()

        if self.frame_count == 0:
            self.frame_start = pred
            logging.info("Receiver: frame starts at = %s", pred)
        elif self.frame_count == self.frame - 1:
            self.frame_end = pred
            logging.info("Receiver: frame ends at = %s", pred)

            if self.frame_start + DELTA < self.frame_end:
                self.bit = 1
            else:
                self.bit = 0
            logging.info("Receiver: RECEIVED: %s", self.bit)
        else:
            pass

        self.frame_count = (self.frame_count + 1) % self.frame


    def calibrate(self):
        self.frame += 1

    def craft(self):
        found = False
        s = 0
        label = self.bias_prediction()
        while not found and s < FUZZMAX:
            image = 
        seven2one()

class Observer(Client):

    def __init__(self,x_bias0,x_bias1,y_label):
        self.frame_count = 0
        self.frame = 0
        self.x = 0
        x_train = numpy.array([x_sample,x_biased])
        y_train = numpy.array([y_label,y_label])
        x_train = x_train.astype('float32')
        x_train /= 255
        super().__init__("Observer",x_train, y_train, x_train, y_train)

    # Covert channel send
    def call_training(self,n_of_epoch):
        pass

    def set_frame(self, frame):
        self.frame = frame

    def update_model_weights(self,main_model):
        logging.debug("Observer: update_model_weights()")
        super().update_model_weights(main_model)
        pred = self.bias_prediction()

        logging.debug("Observer: global prediction = %s, frame_count = %s", pred, self.frame_count)

        update_plot(self.x, pred)
        log_score(self.x, pred)

        if self.frame > 0:
            if self.frame_count == 0:
                add_vline(self.x)
                log_event(self.x, 'Frame start')
            self.frame_count = (self.frame_count + 1) % self.frame

        self.x += 1

    def bias_prediction(self):
        x_pred = self.x_train[[1]]
        prediction = self.predict(x_pred)
        return prediction[0][LABEL]

def global_bias_prediction(server, client):
    x_pred = client.x_train[[1]]
    prediction = server.predict(x_pred)
    return prediction[0][LABEL]

def main():
    # 1. parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("conf_file",type=str)
    args = parser.parse_args()

    # 2. create Setup
    setup = Setup(args.conf_file)

    # 2.1. add observer
    observer = Observer(ORIGINAL, BASELINE, LABEL)
    setup.add_clients(observer)

    # 3. run N rounds OR load pre-trained models
    setup.run(federated_runs=NTRAIN)
    #setup.load("...")

    # 4. create Receiver
    receiver = Receiver(ORIGINAL, BASELINE, LABEL)
    setup.add_clients(receiver)
    log_event(observer.x, 'Receiver added')

    # 5. compute channel baseline
    # baseline = receiver.compute_baseline()
    while receiver.state != ReceiverState.Ready or receiver.frame_count != 0:
        setup.run(federated_runs=1)
        # pred = global_bias_prediction(setup.server, observer)
        # logging.info("SERVER: global prediction = %s", pred)

    logging.info("Attacker: ready to transmit with frame size %s", receiver.frame)

    # 6. create sender
    sender = Sender(ORIGINAL, BASELINE, LABEL,receiver.frame,receiver.replay_model)
    setup.add_clients(sender)
    log_event(observer.x, 'Sender added')
    observer.set_frame(receiver.frame)

    # 7. perform channel calibration

    # 8. start transmitting
    successful_transmissions = 0
    for r in range(NTRANS):
        logging.info("Attacker: starting transmission frame")
        setup.run(federated_runs=receiver.frame)
        successful_transmissions += check_transmission_success(sender, receiver)
        log_event(observer.x, "Transmissions: " + str(successful_transmissions))

    logging.info("ATTACK TERMINATED: %s/%s bits succesfully transimitted", successful_transmissions, NTRANS)
    plt.savefig('output.png', dpi=300)

    sdf = pandas.DataFrame(score_dict)
    sdf.to_csv(SCORE_LOG)
    edf = pandas.DataFrame(event_dict)
    edf.to_csv(EVENT_LOG)

def check_transmission_success(s, r):
    result = 0
    if s.bit != None:
        if s.bit == r.bit:
            logging.info("Attacker: transmission SUCCESS")
            result = 1
        else:
            logging.info("Attacker: transmission FAIL")
        s.bit = None
        r.bit = None
    return result

if __name__ == '__main__':
    logging.basicConfig(format='[+] %(levelname)s: %(message)s', level=logging.INFO)
    main()

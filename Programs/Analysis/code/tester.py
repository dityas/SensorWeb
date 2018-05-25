import logging
import numpy
from sklearn.metrics import mean_absolute_error, recall_score, f1_score
from sklearn.neighbors import LocalOutlierFactor
from models import flat_generator
import matplotlib.pyplot as plotter
import pandas


class Tester:

    def __init__(self, test_set, model, window, model_name,
                 store_dir="images/"):
        self.base_set = test_set
        self.logger = logging.getLogger(self.__class__.__name__)
        self.model = model
        self.window = window
        self.store_dir = store_dir
        self.model_name = model_name
        self.logger.info(f"Starting tests with {self.model_name}")

    def __run_model(self, data, ravel=1):

        """
            Run the forward pass of the model.
        """

        test_gen = flat_generator(numpy.array([data]), self.window, 0)
        error = []
        targets = []
        preds = []

        for i in range(data.shape[0]-(self.window+1)):
            _input, target = next(test_gen)
            targets.append(target.squeeze())
        #print(_input.shape)
            if ravel:
                _input = _input.ravel()[:, numpy.newaxis].T

            pred = self.model.predict(_input)
            # print(target.shape)
            # print(pred.shape)
            preds.append(pred.squeeze())
            #print(numpy.array(preds).shape)
            error.append(mean_absolute_error(y_pred=pred,
                                             y_true=target))

        targets = numpy.vstack(targets)
        preds = numpy.vstack(preds)
        # differences = numpy.abs(targets-preds)
        # print(numpy.array(error).shape)
        return numpy.array(error).squeeze()

    def run_tests(self):

        for i in range(1, 200):

            # Anomaly width test
            self.do_width_test()
            break

    def __run_LOF(self, data):
        clf = LocalOutlierFactor(n_neighbors=100, metric='euclidean')
        data = numpy.array(data)
        data = data[:, numpy.newaxis]
        outliers = clf.fit_predict(data)
        outliers = 1.0 * (outliers < 0)
        return outliers

    def __run_CAD(self, data, start=50, thres=6):

        data = pandas.Series(data)
        running_mean = data.expanding().mean()
        running_std = data.expanding().std()
        alarm = numpy.zeros_like(data)
        s_h = 0
        for i in range(len(data)):
            if i < start:
                continue

            mean, std = running_mean[i], running_std[i]
            val = max(0, s_h + data[i] - mean - std)

            if val > thres * std:
                alarm[i] = 1.0
            else:
                s_h = val
        #plotter.plot(data, alpha=0.3)
        #plotter.plot(data, alpha=0.3)
        #plotter.plot(alarm)
        #plotter.show()

        return alarm

    def __run_Chebyshev(self, data):

        arr = pandas.Series(data)
        mean = 0
        count = 0
        outliers = numpy.zeros_like(arr)
        thres = numpy.zeros_like(arr)
        means = numpy.zeros_like(arr)
        cmeans = arr.expanding().mean()
        std = 0

        # Compute running stats

        m2 = 0
        for i in range(len(arr)):

            if i > 100 and arr[i] > (mean + 5 * std):
                outliers[i] = 1.0
                means[i] = mean
                thres[i] = mean + (5 * std)
                continue

            count = count + 1
            delta = arr[i] - mean

            mean = mean + (delta/count)
            means[i] = mean

            new_delta = arr[i] - mean
            m2 = m2 + delta * new_delta

            std = numpy.sqrt(m2 / count)

            thres[i] = mean + (5 * std)

        # mark = numpy.zeros(arr.shape[0])

        # window = 100
        #
        # for i in range(window, outlier.shape[0]):
        #     num = window
        #     outliers = numpy.sum(outlier[i-window:i])
        #     per = outliers/num
        #     if per > 0.04:
        #         mark[i-window:i] = outlier[i-window:i]
        #     else:
        #         mark[i] = 0.0

        return outliers

    def store_plot(self, plots, names, duration, name):
        # plotter.figure()
        # plotter.title(f"{self.model_name}_{self.window}_{name}.png")
        # plotter.subplot(311)
        # plotter.plot(plots[0], label=names[0], linewidth=0.5)
        # plotter.xlabel("Time")
        # plotter.legend()
        # plotter.subplot(312)
        # plotter.plot(plots[1], label=names[1], linewidth=0.5)
        # plotter.xlabel("Time")
        # plotter.legend()
        # plotter.subplot(313)
        # plotter.plot(plots[2], label=names[2], linewidth=0.5)
        # plotter.xlabel("Time")
        # plotter.legend()
        _name = f"{self.store_dir}/{self.model_name}_{duration}_{name}.png"
        # self.logger.info(f"Saving figure {_name}")
        # plotter.savefig(_name, dpi=500)
        # plotter.close()
        truth = plots[1]
        alarms = plots[2]
        f1 = f1_score(y_true=truth, y_pred=alarms)
        recall = recall_score(y_true=truth, y_pred=alarms)
        self.logger.info(f"For {_name}, f1 is {f1}, recall is {recall}")

    def do_width_test(self):

        for width in range(1, 20):

            net_dataset = numpy.copy(self.base_set)
            cpu_dataset = numpy.copy(self.base_set)
            anomaly_range = numpy.random.randint(3000, 5000)
            true = numpy.zeros(self.base_set.shape[0])

            # Create synthetic anomalies in network and CPU usage.
            net_dataset[anomaly_range: anomaly_range+width, 21: 23] = 1.0
            cpu_dataset[anomaly_range: anomaly_range+width, 0] = 0.0
            cpu_dataset[anomaly_range: anomaly_range+width, 6] = 1.0
            true[anomaly_range: anomaly_range+width] = 1.0

            # Run prediction loop on synthetic data.
            self.logger.debug(f"Running prediction on network flow attack anomaly duration {width}")
            net_error = self.__run_model(net_dataset)
            self.logger.debug(f"Running prediction on CPU busy anomaly duration {width}")
            cpu_error = self.__run_model(cpu_dataset)

            net_alarms = self.__run_CAD(numpy.array(net_error))

            self.store_plot([net_error,
                             true[len(true)-len(net_error):],
                             net_alarms],
                            ["error",
                             "truth",
                             "alarms"], width, "net_cad")

            cpu_alarms = self.__run_CAD(numpy.array(cpu_error))

            self.store_plot([net_error,
                             true[len(true)-len(cpu_error):],
                             cpu_alarms],
                            ["error",
                             "truth",
                             "alarms"], width, "cpu_cad")

            net_alarms = self.__run_Chebyshev(numpy.array(net_error))

            self.store_plot([net_error,
                             true[len(true)-len(net_error):],
                             net_alarms],
                            ["error",
                             "truth",
                             "alarms"], width, "net_chb")

            cpu_alarms = self.__run_Chebyshev(numpy.array(cpu_error))

            self.store_plot([net_error,
                             true[len(true)-len(cpu_error):],
                             cpu_alarms],
                            ["error",
                             "truth",
                             "alarms"], width, "cpu_chb")

            net_alarms = self.__run_LOF(numpy.array(net_error))

            self.store_plot([net_error,
                             true[len(true)-len(net_error):],
                             net_alarms],
                            ["error",
                             "truth",
                             "alarms"], width, "net_lof")

            cpu_alarms = self.__run_LOF(numpy.array(cpu_error))

            self.store_plot([net_error,
                             true[len(true)-len(cpu_error):],
                             cpu_alarms],
                            ["error",
                             "truth",
                             "alarms"], width, "cpu_lof")

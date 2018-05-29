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

    def random_tests(self,
                     width):

        errors = []
        trues = []
        cads = []
        chbs = []
        lofs = []

        for i in range(30):
            self.logger.debug(f"Running iteration {i} of 30")
            anomaly_range = numpy.random.randint(3000, 5000)
            anomalous_series = numpy.random.randint(0, 28)
            sample = numpy.copy(self.base_set)
            true = numpy.zeros(sample.shape[0])
            sample[anomaly_range:anomaly_range + width, anomalous_series] = 1.0
            sample[anomaly_range:anomaly_range + width, anomalous_series + 1] = 1.0
            true[anomaly_range:anomaly_range + width] = 1.0

            error = self.__run_model(data=sample)
            true = true[len(true) - len(error):]

            cads.append(self.__run_CAD(data=error))
            chbs.append(self.__run_Chebyshev(data=error))
            lofs.append(self.__run_LOF(data=error))
            trues.append(true)

        cads = numpy.stack(cads, axis=0)
        chbs = numpy.stack(chbs, axis=0)
        lofs = numpy.stack(lofs, axis=0)
        trues = numpy.stack(trues, axis=0)

        cads_f1 = f1_score(y_true=trues.ravel(), y_pred=cads.ravel())
        chbs_f1 = f1_score(y_true=trues.ravel(), y_pred=chbs.ravel())
        lofs_f1 = f1_score(y_true=trues.ravel(), y_pred=lofs.ravel())

        cads_re = recall_score(y_true=trues.ravel(), y_pred=cads.ravel())
        chbs_re = recall_score(y_true=trues.ravel(), y_pred=chbs.ravel())
        lofs_re = recall_score(y_true=trues.ravel(), y_pred=lofs.ravel())

        self.logger.info(f"For width {width} CAD f1 is {cads_f1}")
        self.logger.info(f"For width {width} CAD re is {cads_re}")
        self.logger.info(f"For width {width} Cheb f1 is {chbs_f1}")
        self.logger.info(f"For width {width} Cheb re is {chbs_re}")
        self.logger.info(f"For width {width} LOF f1 is {lofs_f1}")
        self.logger.info(f"For width {width} LOF re is {lofs_re}")

        return {"cads_f1": cads_f1,
                "chbs_f1": chbs_f1,
                "lofs_f1": lofs_f1,
                "cads_re": cads_re,
                "chbs_re": chbs_re,
                "lofs_re": lofs_re}

    def do_width_test(self):

        cad_f1s = []
        chb_f1s = []
        lof_f1s = []
        cad_res = []
        chb_res = []
        lof_res = []
        widths = []

        for width in range(1, 20):

            results = self.random_tests(width=width)

            cad_f1s.append(results["cads_f1"])
            chb_f1s.append(results["chbs_f1"])
            lof_f1s.append(results["lofs_f1"])
            cad_res.append(results["cads_re"])
            chb_res.append(results["chbs_re"])
            lof_res.append(results["lofs_re"])
            widths.append(width)

        f1_name = f"{self.store_dir}/{self.model_name}_{width}_f1_.png"
        re_name = f"{self.store_dir}/{self.model_name}_{width}_re_.png"

        plotter.figure()
        plotter.plot(cad_f1s, widths, 'r', label="CUSUM", linewidth=0.5)
        plotter.plot(chb_f1s, widths, 'g', label="Chebyshev", linewidth=0.5)
        plotter.plot(chb_f1s, widths, 'b', label="LOF", linewidth=0.5)
        plotter.ylabel("f1 score")
        plotter.xlabel("anomaly width")
        plotter.ylim(0, 1)
        plotter.legend()
        plotter.savefig(f1_name, dpi=500)

        self.logger.info(f"Saved f1 score plot {f1_name}")

        plotter.figure()
        plotter.plot(cad_res, widths, 'r', label="CUSUM", linewidth=0.5)
        plotter.plot(chb_res, widths, 'g', label="Chebyshev", linewidth=0.5)
        plotter.plot(chb_res, widths, 'b', label="LOF", linewidth=0.5)
        plotter.ylabel("recall score")
        plotter.xlabel("anomaly width")
        plotter.ylim(0, 1)
        plotter.legend()
        plotter.savefig(re_name, dpi=500)

        self.logger.info(f"Saved recall score plot {re_name}")

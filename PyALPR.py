import json, shlex, subprocess

class PlateReader:


    def __init__(self):
        #webcam subprocess args
        webcam_command = "fswebcam -r 640x480 -S 20 --no-banner --quiet alpr.jpg"
        self.webcam_command_args = shlex.split(webcam_command)

        #alpr subprocess args
        alpr_command = "alpr -c eu -t hr -n 300 -j alpr.jpg"
        self.alpr_command_args = shlex.split(alpr_command)


    def webcam_subprocess(self):
        return subprocess.Popen(self.webcam_command_args, stdout=subprocess.PIPE)


    def alpr_subprocess(self):
        return subprocess.Popen(self.alpr_command_args, stdout=subprocess.PIPE)


    def alpr_json_results(self):
        self.webcam_subprocess().communicate()
        alpr_out, alpr_error = self.alpr_subprocess().communicate()

        if not alpr_error is None:
            return None, alpr_error
        elif "No license plates found." in alpr_out:
            return None, None

        try:
            return json.loads(alpr_out), None
        except ValueError, e:
            return None, e


    def read_plate(self):
        alpr_json, alpr_error = self.alpr_json_results()

        if not alpr_error is None:
            print alpr_error
            return

        if alpr_json is None:
            print "No results!"
            return

        results = alpr_json["results"]

        print "Total results: %d" % len(results)

        order = 0
        for result in results:
            matches_template = result["matches_template"]
            if matches_template == 1:
                plate = result["plate"]
                order += 1
                print "Plate {0:d}: {1:s} {2:.2f}".format(order, plate, result["confidence"])

            candidates = result["candidates"]

            print "Total candidates: %d" % len(candidates)

            order = 0
            for candidate in candidates:
                matches_template = candidate["matches_template"]
                if matches_template == 1:
                    plate = candidate["plate"]
                    order += 1
                    print "Plate {0:d}: {1:s} {2:.2f}".format(order, plate, candidate["confidence"])

        print "------------"





if __name__=="__main__":
    plate_reader = PlateReader()
    plate_reader.read_plate()
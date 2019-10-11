import os, json


class MediaExplorer:

    media_files = [ ".mkv", ".avi", ".mpeg", ".mpg", ".mp4" ]

    def __init__(self, path):
        self.path = path

    def explore_shows(self):
        return self.explore_results( self.path + '/Entertainment/Shows/', True )

    def explore_movies(self):
        return self.explore_results( self.path + '/Movies/' )

    def explore_results(self, path, hierarchy=False):
        data = self.explore_single( path )
        results = {}

        for directory, files in data.iteritems():
            extras = {}

            if hierarchy:
                extras["season"] = directory.split('/').pop()
                name = directory.split('/')[-2]
            else:
                name = os.path.basename(directory)

            lines = {}

            for single in files:
                for ext in self.media_files:
                    if str(single).endswith(ext):
                        entry = {}
                        entry["file"] = single
                        entry["ext"] = ext
                        stat = os.stat(os.path.join(directory, single))
                        entry["size"] = stat.st_size
                        entry["mtime"] = stat.st_mtime
                        entry["ctime"] = stat.st_ctime
                        entry["directory"] = str(directory).replace(self.path, "")

                        if extras:
                            for e, v in extras.iteritems():
                                entry[e] = v

                        has_subtitle = False
                        for of in files:
                            if str(of) == str(single).replace(ext, ".srt"):
                                has_subtitle = True

                        entry["subtitle"] = has_subtitle

                        lines[ str(single).replace(ext, "") ] = entry

            results[name] = lines

        return results


    def explore_single(self, dir):
        results = {}
        result_limit = 400
        result_count = 0

        for dirname, dirnames, filenames in os.walk(dir):
            filenames = [f for f in filenames if not f[0] == '.']
            dirnames[:] = [d for d in dirnames if not d[0] == '.']

            if len(filenames) > 0:
                results[dirname] = []
                for s in filenames:
                    results[dirname].append(str(s))
                    result_count += 1

                    if result_count == result_limit:
                        return results

    def explore(self):
        data = {
                    #"shows": self.explore_shows(),
                    "movies": self.explore_movies()
                }

        return data


results = MediaExplorer("/Volumes/Media/").explore()

with open('explorer_results.json', 'w') as outfile:
    json.dump(results, outfile)

print "Done - saved content to explorer_results.json file."

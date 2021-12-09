import json
import johnnydep
import wget
import os
import argparse


class PackageInfo:
    def __init__(self, name, summary, depth):
        self.name = name
        self.summary = summary
        self.dept = depth

# mavproxy
def parse_arguments():
    parser = argparse.ArgumentParser(description='find and download all dependent whl files of package')

    parser.add_argument('-n', '--package_name', default='',
                        help='package name', required=True)

    return parser.parse_args()

def __main__():
    parser = parse_arguments()
    package_name = parser.package_name
    print('Finding dep {}'.format(package_name))
    j = johnnydep.JohnnyDist(package_name)

    deepest = 0
    package_info_list = [PackageInfo(name=j.name, summary=j.summary, depth=j.depth).__dict__]
    download_links = [j.download_link]

    out_str = '{}: {} \n'.format(j.name, j.summary)
    for curr in j.descendants:
        download_links.append(curr.download_link)
        if curr.depth > deepest:
            deepest = curr.depth
        package_info_list.append(PackageInfo(name=curr.name, summary=curr.summary, depth=curr.depth).__dict__)
        for i in range(curr.depth):
            out_str = out_str + '----'
        out_str = out_str + '{}: {} \n'.format(curr.name, curr.summary)

    package_json = {'package': [{'name': package_name, 'deepest': deepest}, package_info_list]}

    json_out = json.dumps(package_json, indent=4)
    out_str = json_out

    for link in download_links:
        print("installing {}".format(link))
        wget.download(link, os.getcwd())

    open(os.path.join(os.getcwd(), 'dependency_tree.json'), "w").write(out_str)


__main__()




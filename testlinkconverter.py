import sys
from lxml import etree
import csv

if len(sys.argv) == 1:
    print "Please input CSV file path."
    sys.exit(1)
file_path = sys.argv[1]


class BaseTestLinkObject(object):
    node_order = ""
    details = ""

    def __str__(self):
        return self.node_order + " " + self.details

class TestCaseStep(object):
    step_number = ""
    actions = ""
    expectedresults = ""
    execution_type = "1"

    def __str__(self):
        return self.step_number + " " + self.actions + " " + self.expectedresults + " " + self.execution_type


class TestCase(BaseTestLinkObject):
    internalid = 1
    name = ""
    summary = ""
    preconditions = ""
    execution_type = "1"
    importance = ""
    estimated_exec_duration = ""
    status = 1
    is_open = 1
    active = 1
    steps = None

    def __str__(self):
        return str(self.internalid) + " " + self.name + "\n" + self.details + "\n" + self.summary + "\n" + self.preconditions


class TestSuite(BaseTestLinkObject):

    id = ""
    name = ""
    test_cases = None

    def __str__(self):
        return str(self.node_order) + " " + self.name + " " + str(self.id) + "\n " + self.details


with open(file_path) as f:
    lines = csv.reader(f)
    root = etree.Element('testsuite')
    root.attrib["id"] = ""
    root.attrib["name"] = ""
    root_no = etree.SubElement(root, 'node_order')
    root_no.text = etree.CDATA("")
    root_det = etree.SubElement(root, 'details')
    root_det.text = etree.CDATA("")
    id_count = 10
    test_suite_node_order = 10

    TEST_SUITE_START = 0
    TEST_SUITE_SUMMARY = 1
    TEST_CASE_START = 2
    TEST_CASE_AUTHOR = 3
    TEST_CASE_EDITTED_BY = 4
    TEST_CASE_SUMMARY = 5
    TEST_CASE_PRECONDITIONS = 6
    TEST_CASE_STEP_TITLE = 7
    TEST_CASE_STEP = 8
    TEST_CASE_EXECUTION_TYPE = 9
    TEST_CASE_EXEC_DURATION = 10
    TEST_CASE_IMPORTANCE = 11
    TEST_CASE_BLANK_ROW = 12
    TEST_CASE_REQ = 15
    TEST_CASE_KEYW = 16
    TEST_CASE_END = 13
    TEST_SUITE_END = 14


    curr_csv_state = TEST_SUITE_START
    test_suites = []
    current_test_suite = None
    current_test_case = None
    current_step = None

    tc_priority_dict = {"Low": 1, "Medium": 2, "High": 3}
    for line in lines:
        # print line
        if "Test Suite : " in line[0]:
            if curr_csv_state == TEST_CASE_END:
                test_suites.append(current_test_suite)
            curr_csv_state = TEST_SUITE_START
        elif curr_csv_state == TEST_CASE_END:
            curr_csv_state = TEST_CASE_START

        if curr_csv_state == TEST_SUITE_START:
            test_suite = TestSuite()
            test_suite.id = id_count
            id_count += 1
            test_suite.name = line[0]
            test_suite.node_order = test_suite_node_order
            test_suite_node_order += 1
            curr_csv_state = TEST_SUITE_SUMMARY
            current_test_suite = test_suite
            continue

        if curr_csv_state == TEST_SUITE_SUMMARY:
            if not "Test Case:" in line[0]:
                current_test_suite.details = line[0]
                curr_csv_state = TEST_CASE_START
                continue
            else:
                test_case = TestCase()
                test_case.internalid = id_count
                id_count += 1
                test_case.name = line[0]
                current_test_case = test_case
                curr_csv_state = TEST_CASE_AUTHOR
                continue

        if curr_csv_state == TEST_CASE_START:
            test_case = TestCase()
            test_case.internalid = id_count
            id_count += 1
            test_case.name = line[0]
            current_test_case = test_case
            curr_csv_state = TEST_CASE_AUTHOR
            continue

        if curr_csv_state == TEST_CASE_AUTHOR:
            curr_csv_state = TEST_CASE_EDITTED_BY
            continue

        if curr_csv_state == TEST_CASE_EDITTED_BY:
            if "#:" in line[0]:
                current_step = TestCaseStep()
                curr_csv_state = TEST_CASE_STEP
                continue
            elif "Preconditions:" in line[0]:
                current_test_case.preconditions = line[0]
                curr_csv_state = TEST_CASE_STEP_TITLE
                continue
            else:
                curr_csv_state = TEST_CASE_SUMMARY
            continue

        if curr_csv_state == TEST_CASE_SUMMARY:
            if "Summary:" in line[0]:
                current_test_case.summary = line[0]
                curr_csv_state = TEST_CASE_PRECONDITIONS
                continue
            elif "Preconditions:" in line[0]:
                current_test_case.preconditions = line[0]
                curr_csv_state = TEST_CASE_STEP_TITLE
                continue
            else:
                current_step = TestCaseStep()
                curr_csv_state = TEST_CASE_STEP
                continue

        if curr_csv_state == TEST_CASE_PRECONDITIONS:
            if "Preconditions:" in line[0]:
                current_test_case.preconditions = line[0]
                curr_csv_state = TEST_CASE_STEP_TITLE
                continue
            else:
                curr_csv_state = TEST_CASE_STEP
                continue

        if curr_csv_state == TEST_CASE_STEP_TITLE:

            curr_csv_state = TEST_CASE_STEP
            continue

        if curr_csv_state == TEST_CASE_STEP:
            if "Execution type" not in line[0]:
                step = TestCaseStep()
                step.step_number = line[0]
                step.actions = line[1]
                step.expectedresults = line[2]
                step.execution_type = "1"
                if not current_test_case.steps:
                    current_test_case.steps = []
                current_test_case.steps.append(step)
                continue
            else:
                curr_csv_state = TEST_CASE_EXEC_DURATION
                continue

        if curr_csv_state == TEST_CASE_EXECUTION_TYPE:
            current_step.execution_type = "1"
            curr_csv_state = TEST_CASE_EXEC_DURATION
            continue

        if curr_csv_state == TEST_CASE_EXEC_DURATION:
            curr_csv_state = TEST_CASE_IMPORTANCE
            continue

        if curr_csv_state == TEST_CASE_IMPORTANCE:
            current_test_case.importance = str(tc_priority_dict[line[1]])
            curr_csv_state = TEST_CASE_BLANK_ROW
            continue

        if curr_csv_state == TEST_CASE_BLANK_ROW:
            curr_csv_state = TEST_CASE_REQ
            continue

        if curr_csv_state == TEST_CASE_REQ:
            curr_csv_state = TEST_CASE_KEYW
            continue

        if curr_csv_state == TEST_CASE_KEYW:
            curr_csv_state = TEST_CASE_END
            if not current_test_suite.test_cases:
                current_test_suite.test_cases = []
            current_test_suite.test_cases.append(current_test_case)
            continue

    if curr_csv_state == TEST_CASE_END:
        test_suites.append(current_test_suite)

    root = etree.Element('testsuite')
    root.attrib["id"] = ""
    root.attrib["name"] = ""
    node_order = etree.SubElement(root, "node_order")
    node_order.text = etree.CDATA("")
    details = etree.SubElement(root, "details")
    details.text = etree.CDATA("")
    for ts in test_suites:
        ts_root = etree.SubElement(root, 'testsuite')
        ts_root.attrib["id"] = str(ts.id)
        ts_root.attrib["name"] = ts.name
        ts_no = etree.SubElement(ts_root, 'node_order')
        ts_no.text = etree.CDATA(str(ts.node_order))
        ts_details = etree.SubElement(ts_root, 'details')
        ts_details.text = etree.CDATA(ts.details)
        # print ts
        for tc in ts.test_cases:
            tc_root = etree.SubElement(ts_root, "testcase")

            tc_root.attrib["internalid"] = str(tc.internalid)

            tc_root.attrib["name"] = tc.name

            tc_no = etree.SubElement(tc_root, "node_order")
            tc_no.text = etree.CDATA("1000")

            tc_version = etree.SubElement(tc_root, "version")
            tc_version.text = etree.CDATA("1")

            tc_summary = etree.SubElement(tc_root, "summary")
            tc_summary.text = etree.CDATA(tc.summary)

            tc_preconditions = etree.SubElement(tc_root, "preconditions")
            tc_preconditions.text = etree.CDATA(tc.preconditions)

            tc_execution_type = etree.SubElement(tc_root, "execution_type")
            tc_execution_type.text = etree.CDATA(tc.execution_type)

            tc_importance = etree.SubElement(tc_root, "importance")
            tc_importance.text = etree.CDATA(tc.importance)

            tc_estimated_exec_duration = etree.SubElement(tc_root, "estimated_exec_duration")

            tc_status = etree.SubElement(tc_root, "status")
            tc_status.text = "1"

            tc_is_open = etree.SubElement(tc_root, "is_open")
            tc_is_open.text = "1"

            tc_active = etree.SubElement(tc_root, "active")
            tc_active.text = "1"

            # print tc
            steps = etree.SubElement(tc_root, "steps")
            if tc.steps:
                for s in tc.steps:
                    step = etree.SubElement(steps, "step")

                    step_num = etree.SubElement(step, "step_number")
                    step_num.text = etree.CDATA(s.step_number)

                    actions = etree.SubElement(step, "actions")
                    actions.text = etree.CDATA(s.actions)

                    expectedresults = etree.SubElement(step, "expectedresults")
                    expectedresults.text = etree.CDATA(s.expectedresults)

                    execution_type = etree.SubElement(step, "execution_type")
                    execution_type.text = etree.CDATA(s.execution_type)

    print etree.tostring(root)









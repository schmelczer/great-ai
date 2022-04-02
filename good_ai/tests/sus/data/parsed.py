from sus.publication_tei.models import (
    Affiliation,
    Author,
    Meta,
    Paragraph,
    PublicationMetadata,
    Text,
    Title,
)

metadata = PublicationMetadata(
    language="en",
    title="Spiritual dimension in palliative medicine: a qualitative study of learning tasks: medical students, teachers, educationalists",
    publisher="BMJ",
    doi="10.1136/bmjspcare-2021-003026",
    md5="EAE447B92E88C8C72D4610586A269870",
    publication_date="2021-07-20",
    keywords=[],
    reference_count=34,
)

authors = [
    Author(
        name="Ms Jolien Pieters",
        orcid="0000-0002-9327-3977",
        email="j.pieters@maastrichtuniversity.nl",
        corresponding=True,
        affiliations=[
            Affiliation(
                institutions=["Maastricht University"],
                departments=[
                    "Department of Educational Development and Research",
                    "Faculty of Health, Medicine and Life Sciences",
                    "School of Health Professions Education",
                ],
                laboratories=[],
                country="The Netherlands",
                settlement="Maastricht",
            )
        ],
        coordinates="1,166.78,184.02,67.25,10.43",
    ),
    Author(
        name="Daniëlle Verstegen",
        orcid=None,
        email=None,
        corresponding=False,
        affiliations=[
            Affiliation(
                institutions=["Maastricht University"],
                departments=[
                    "Department of Educational Development and Research",
                    "Faculty of Health, Medicine and Life Sciences",
                    "School of Health Professions Education",
                ],
                laboratories=[],
                country="The Netherlands",
                settlement="Maastricht",
            )
        ],
        coordinates="1,261.76,184.02,94.40,10.43",
    ),
    Author(
        name="Diana Dolmans",
        orcid=None,
        email=None,
        corresponding=False,
        affiliations=[
            Affiliation(
                institutions=["Maastricht University"],
                departments=[
                    "Department of Educational Development and Research",
                    "Faculty of Health, Medicine and Life Sciences",
                    "School of Health Professions Education",
                ],
                laboratories=[],
                country="The Netherlands",
                settlement="Maastricht",
            )
        ],
        coordinates="1,368.73,184.02,74.73,10.43",
    ),
    Author(
        name="Evelien Neis",
        orcid=None,
        email=None,
        corresponding=False,
        affiliations=[
            Affiliation(
                institutions=["Maastricht University"],
                departments=[
                    "Department of Educational Development and Research",
                    "Faculty of Health, Medicine and Life Sciences",
                    "School of Health Professions Education",
                ],
                laboratories=[],
                country="The Netherlands",
                settlement="Maastricht",
            )
        ],
        coordinates="1,456.53,184.02,59.31,10.43",
    ),
    Author(
        name="Franca Warmenhoven",
        orcid=None,
        email=None,
        corresponding=False,
        affiliations=[
            Affiliation(
                institutions=["Maastricht University"],
                departments=[
                    "Department of Educational Development and Research",
                    "Faculty of Health, Medicine and Life Sciences",
                    "School of Health Professions Education",
                ],
                laboratories=[],
                country="The Netherlands",
                settlement="Maastricht",
            )
        ],
        coordinates="1,166.77,197.02,108.77,10.43",
    ),
    Author(
        name="Marieke Van Den Beuken-Van Everdingen",
        orcid=None,
        email=None,
        corresponding=False,
        affiliations=[
            Affiliation(
                institutions=[],
                departments=["Centre of Expertise for Palliative Care"],
                laboratories=["UMC+"],
                country="The Netherlands",
                settlement="Maastricht, Maastricht",
            )
        ],
        coordinates="1,289.21,197.02,210.89,10.43",
    ),
    Author(
        name=None,
        orcid=None,
        email=None,
        corresponding=False,
        affiliations=[
            Affiliation(
                institutions=["Maastricht University"],
                departments=[
                    "Department of Educational Development and Research",
                    "Faculty of Health, Medicine and Life Sciences",
                ],
                laboratories=[],
                country="The Netherlands",
                settlement="Maastricht",
            )
        ],
        coordinates=None,
    ),
]

content = [
    Meta(meta_type="abstract_start"),
    Paragraph(
        sentences=[
            Text(
                content="Background Palliative care is gaining importance within the physician's range of duties.",
                document_order=0,
                coordinates="1,166.78,241.37,137.11,8.06;1,166.78,253.96,153.49,8.06;1,166.78,266.56,24.09,8.06",
            ),
            Text(
                content="In the undergraduate medical curriculum, education on the four dimensions of care is insufficient.",
                document_order=1,
                coordinates="1,193.23,266.56,150.18,8.06;1,166.78,279.16,157.13,8.06;1,166.78,291.76,41.88,8.06",
            ),
            Text(
                content="The spiritual dimension is hardly addressed.",
                document_order=2,
                coordinates="1,211.02,291.76,115.56,8.06;1,166.78,304.35,38.58,8.06",
            ),
            Text(
                content="Therefore, we developed a coherent set of learning tasks targeted at learning to communicate about the spiritual dimension.",
                document_order=3,
                coordinates="1,207.72,304.35,130.84,8.06;1,166.78,316.95,156.63,8.06;1,166.78,329.55,159.63,8.06",
            ),
            Text(
                content="The learning tasks are based on educational principles of authentic learning, reflective learning and longitudinal integration in the curriculum.",
                document_order=4,
                coordinates="1,166.78,342.14,158.70,8.06;1,166.78,354.74,149.23,8.06;1,166.78,367.34,156.03,8.06;1,166.78,379.93,40.60,8.06",
            ),
            Text(
                content="This article reports on the feasibility of using these learning tasks in the medical curricula.",
                document_order=5,
                coordinates="1,209.74,379.93,127.81,8.06;1,166.78,392.53,156.48,8.06;1,166.78,405.13,33.05,8.06",
            ),
            Text(
                content="Methods Teachers and educational scientists were interviewed and students were asked to evaluate the learning tasks in focus groups.",
                document_order=6,
                coordinates="1,166.78,417.73,165.28,8.06;1,166.78,430.32,164.53,8.06;1,166.78,442.92,156.81,8.06",
            ),
            Text(
                content="Interview transcripts were analysed by three independent researchers.",
                document_order=7,
                coordinates="1,166.78,455.52,158.35,8.06;1,166.78,468.11,90.85,8.06",
            ),
        ]
    ),
    Title(
        text=Text(
            content="Results",
            document_order=8,
            coordinates="1,166.78,480.71,28.33,8.06",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="The learning tasks encourage the students to reflect on the four dimensions of palliative care and their personal values.",
                document_order=9,
                coordinates="1,199.36,480.71,120.12,8.06;1,166.78,493.31,161.86,8.06;1,166.78,505.90,143.88,8.06",
            ),
            Text(
                content="Learning was clearly organised around authentic learning tasks relevant to the later profession, using paper, video cases, as well as simulations and real patients.",
                document_order=10,
                coordinates="1,313.02,505.90,31.32,8.06;1,166.78,518.50,173.33,8.06;1,166.78,531.10,155.07,8.06;1,166.78,543.70,163.58,8.06;1,166.78,556.29,46.60,8.06",
            ),
            Text(
                content="Participants suggest giving more attention to cultural diversity.",
                document_order=11,
                coordinates="1,215.74,556.29,116.97,8.06;1,166.78,568.89,105.46,8.06",
            ),
            Text(
                content="As palliative care is an emotionally charged subject, the safety of both student and patient should be guaranteed.",
                document_order=12,
                coordinates="1,274.60,568.89,60.28,8.06;1,166.78,581.49,170.48,8.06;1,166.78,594.08,174.79,8.06",
            ),
            Text(
                content="All participants indicated that the program should start in the bachelor phase and most agreed that it should be integrated vertically and horizontally throughout the undergraduate program, although there is some debate about the optimal moment to start.",
                document_order=13,
                coordinates="1,166.78,606.68,153.80,8.06;1,166.78,619.28,159.18,8.06;1,166.78,631.87,159.94,8.06;1,166.78,644.47,172.25,8.06;1,166.78,657.07,169.74,8.06;1,166.78,669.67,105.31,8.06",
            ),
            Text(
                content="Conclusion The tasks, are authentic, encourage the students to reflect on the spiritual dimension of palliative care and are suitable for integration in the undergraduate medical curriculum.",
                document_order=14,
                coordinates="1,166.78,682.26,176.47,8.06;1,166.78,694.86,176.02,8.06;1,166.78,707.46,173.48,8.06;1,166.78,720.05,150.18,8.06",
            ),
        ]
    ),
    Title(
        text=Text(
            content="Key messages",
            document_order=15,
            coordinates="1,366.28,233.91,57.96,9.48",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="What was already known?",
                document_order=16,
                coordinates="1,366.28,256.11,104.45,9.01",
            ),
            Text(
                content="► Insufficient education on four dimensions of palliative care in undergraduate medical curriculum.",
                document_order=17,
                coordinates="1,366.27,267.11,160.84,9.23;1,378.28,278.11,154.38,9.01;1,378.28,289.11,40.11,9.01",
            ),
            Text(
                content="► Especially the spiritual dimension is hardly addressed.",
                document_order=18,
                coordinates="1,366.27,300.11,164.09,9.23;1,378.28,311.11,38.66,9.01",
            ),
        ]
    ),
    Title(
        text=Text(
            content="What are the new findings?",
            document_order=19,
            coordinates="1,366.28,328.11,109.39,9.01",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="► A coherent set of learning tasks developed in line with instructional design guidelines.",
                document_order=20,
                coordinates="1,366.27,339.11,165.32,9.23;1,378.28,350.11,153.86,9.01",
            ),
            Text(
                content="► Stakeholder evaluations positive; confirm that these are authentic and encourage reflection.",
                document_order=21,
                coordinates="1,366.27,361.11,159.56,9.23;1,378.28,372.11,141.75,9.01;1,378.28,383.11,36.05,9.01",
            ),
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="What is their significance?",
                document_order=22,
                coordinates="1,366.28,400.11,104.57,9.01",
            ),
            Text(
                content="a. Clinical: Enhances palliative care education for medical students.",
                document_order=23,
                coordinates="1,366.28,411.11,166.50,9.01;1,378.28,422.11,75.08,9.01",
            ),
            Text(
                content="b.", document_order=24, coordinates="1,366.28,433.11,6.50,9.01"
            ),
            Text(
                content="Research: Suitable for integration in undergraduate medical curriculum.",
                document_order=25,
                coordinates="1,378.28,433.11,128.72,9.01;1,378.28,444.11,125.74,9.01",
            ),
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="copyright.",
                document_order=26,
                coordinates="1,567.14,376.44,8.32,39.01",
            )
        ]
    ),
    Meta(meta_type="abstract_end"),
    Title(
        text=Text(
            content="INTRODUCTION",
            document_order=27,
            coordinates="1,360.28,486.04,71.51,9.24",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="The need for palliative care is set to grow due to demographic changes, longer disease trajectories and higher comorbidity.",
                document_order=28,
                coordinates="1,360.28,498.01,178.54,9.36;1,360.28,510.17,178.57,9.36;1,360.28,522.33,145.45,9.36",
            ),
            Text(
                content="Central to providing palliative care is the holistic, patient-centred and multidimensional approach, which addresses not only the physical, but also the psychological, social and spiritual dimension. 1",
                document_order=29,
                coordinates="1,507.95,522.33,30.90,9.36;1,360.28,534.49,178.57,9.36;1,360.28,546.65,178.56,9.36;1,360.28,558.81,178.60,9.36;1,360.28,570.97,178.57,9.36;1,360.28,583.13,104.24,9.36;1,464.27,580.99,3.69,6.21",
            ),
            Text(
                content="Providing palliative care is increasingly recognised as a universal responsibility of healthcare professionals 2 3 and all doctors will see patients with progressive life-limiting conditions at some point during their careers. 4",
                document_order=30,
                coordinates="1,473.03,583.13,65.74,9.36;1,360.27,595.29,178.56,9.36;1,360.27,607.45,178.58,9.36;1,360.27,619.61,27.60,9.36;1,387.67,617.47,10.12,6.21;1,401.99,619.61,136.83,9.36;1,360.28,631.77,178.53,9.36;1,360.28,643.93,146.67,9.36;1,506.67,641.79,3.69,6.21",
            ),
            Text(
                content="Physicians, irrespective of specialism, should be both competent and confident in caring for the palliative care patient.",
                document_order=31,
                coordinates="1,513.91,643.93,24.87,9.36;1,360.28,656.09,178.57,9.36;1,360.28,668.25,178.57,9.36;1,360.28,680.41,111.83,9.36",
            ),
            Text(
                content="Taking care of palliative care patients is typically associated with powerful and highly emotional situations affecting junior doctor's emotional well-being. 5",
                document_order=32,
                coordinates="1,476.55,680.41,62.29,9.36;1,360.28,692.57,178.57,9.36;1,360.28,704.73,178.50,9.36;1,360.28,716.89,178.58,9.36;1,360.28,729.05,45.08,9.36;1,405.15,726.91,3.69,6.21",
            ),
            Text(
                content="It is therefore important that Original research junior doctors develop the ability to guide palliative care patients during their medical training. 6",
                document_order=33,
                coordinates="1,413.24,729.05,125.59,9.36;2,60.50,24.52,85.87,9.48;2,56.50,45.11,232.01,9.36;2,56.50,57.11,155.00,9.36;2,211.23,54.96,3.69,6.21",
            ),
            Text(
                content="lthough there is a growing international movement to embed palliative care education in the undergraduate medical curricula, 5 this topic is not adequately addressed within all European medical universities.",
                document_order=34,
                coordinates="2,65.50,69.11,222.87,9.36;2,56.50,81.11,231.89,9.36;2,56.50,93.11,101.07,9.36;2,157.56,90.96,3.69,6.21;2,165.88,93.11,122.50,9.36;2,56.50,105.11,231.88,9.36",
            ),
            Text(
                content="Several studies demonstrate that medical students do not receive sufficient education in this area. 7 8",
                document_order=35,
                coordinates="2,56.50,117.11,231.88,9.36;2,56.50,129.11,184.10,9.36;2,240.59,126.96,8.94,6.21",
            ),
            Text(
                content="Students do not feel well prepared [9] [10] [11] [12] and feel especially ill-prepared to raise and discuss the psychological, social and spiritual dimensions of care. 13",
                document_order=36,
                coordinates="2,251.89,129.11,36.49,9.36;2,56.50,141.11,117.08,9.36;2,173.58,138.96,14.37,6.21;2,192.97,141.11,95.43,9.36;2,56.50,153.11,231.90,9.36;2,56.50,165.11,148.73,9.36;2,205.23,162.96,7.37,6.21",
            ),
            Text(
                content="Their education primarily focuses on one dimension-the physicalwhile allowing the others to fall by the wayside. 14",
                document_order=37,
                coordinates="2,217.75,165.11,70.64,9.36;2,56.50,177.11,231.90,9.36;2,56.50,189.11,224.52,9.36;2,281.01,186.96,7.37,6.21",
            ),
            Text(
                content="tudents also report that self-care and reflection in the context of palliative care do not get much attention in their education. 9 13",
                document_order=38,
                coordinates="2,56.50,201.11,231.90,9.36;2,56.50,213.11,231.90,9.36;2,56.50,225.11,67.49,9.36;2,123.99,222.96,12.78,6.21",
            ),
            Text(
                content="In the Netherlands, the undergraduate medical education assigns only limited attention on palliative and end-of-life care. 13 15-17",
                document_order=39,
                coordinates="2,139.37,225.11,149.01,9.36;2,56.50,237.11,231.88,9.36;2,56.50,249.11,146.92,9.36;2,203.41,246.96,28.09,6.21",
            ),
            Text(
                content="This despite that the national competency framework states that the doctor should promote people's health and related quality of life, also in the palliative phase. 18",
                document_order=40,
                coordinates="2,235.51,249.11,52.87,9.36;2,56.50,261.11,231.88,9.36;2,56.50,273.11,231.90,9.36;2,56.50,285.11,172.10,9.36;2,228.59,282.96,7.37,6.21",
            ),
            Text(
                content="The competences that Dutch medical students need to acquire to provide good-quality palliative care have recently been set out in an educational framework. 19",
                document_order=41,
                coordinates="2,237.86,285.11,50.53,9.36;2,56.50,297.11,231.89,9.36;2,56.50,309.11,231.89,9.36;2,56.50,321.11,168.01,9.36;2,224.50,318.96,7.37,6.21",
            ),
            Text(
                content="This framework specifies among others that the medical students should be able to talk to the patient and family about the incurable illness, prognosis and death, and discuss the four dimensions of care.",
                document_order=42,
                coordinates="2,236.71,321.11,51.68,9.36;2,56.50,333.11,231.88,9.36;2,56.50,345.11,231.90,9.36;2,56.50,357.11,231.89,9.36;2,56.50,369.11,121.76,9.36",
            ),
            Text(
                content="They should also be able to take care of their own well-being and reflect on their own spiritual needs, alongside their perceptions about life, death and dying.",
                document_order=43,
                coordinates="2,181.41,369.11,106.99,9.36;2,56.50,381.11,231.88,9.36;2,56.50,393.11,231.89,9.36;2,56.50,405.11,117.74,9.36",
            ),
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="To bridge the gap between what students should learn and actually learn about spiritual care, we developed a coherent set of eight learning tasks.",
                document_order=44,
                coordinates="2,65.50,417.11,222.89,9.36;2,56.50,429.11,231.91,9.36;2,56.50,441.11,182.38,9.36",
            ),
            Text(
                content="Addressing the spiritual dimension is a complex task.",
                document_order=45,
                coordinates="2,241.57,441.11,46.81,9.36;2,56.50,453.11,184.25,9.36",
            ),
            Text(
                content="According to current educational principles, learning complex tasks can be supported by providing authentic or realistic learning tasks 20, by using principles of reflective learning, and should be integrated in the curricula.",
                document_order=46,
                coordinates="2,244.73,453.11,43.66,9.36;2,56.50,465.11,231.90,9.36;2,56.50,477.11,231.90,9.36;2,56.50,489.11,80.12,9.36;2,136.62,486.96,7.37,6.21;2,144.00,489.11,144.40,9.36;2,56.50,501.11,231.89,9.36",
            ),
            Text(
                content="Authentic tasks allow students to acquire knowledge, skills and attitudes in an integrated fashion, 21 which improves the transfer of the curriculum to the workplace. 20",
                document_order=47,
                coordinates="2,56.50,513.11,231.89,9.36;2,56.50,525.11,194.45,9.36;2,250.94,522.96,7.37,6.21;2,262.50,525.11,25.89,9.36;2,56.50,537.11,231.90,9.36;2,56.50,549.11,24.87,9.36;2,81.36,546.96,7.37,6.21",
            ),
            Text(
                content="These authentic learning tasks can be interwoven in existing curricula in a horizontal and vertical integration manner.",
                document_order=48,
                coordinates="2,93.25,549.11,195.14,9.36;2,56.50,561.11,231.90,9.36;2,56.50,573.11,84.74,9.36",
            ),
            Text(
                content="3] [24] [25] Through reflection, students are encouraged to think about their role as a physician, 22 foster professional growth, release the emotional burden of caring for palliative care patients and increase patient care skills. 24",
                document_order=49,
                coordinates="2,91.86,594.96,7.22,6.21;2,101.14,597.11,187.26,9.36;2,56.50,609.11,165.28,9.36;2,221.77,606.96,7.37,6.21;2,231.56,609.11,56.83,9.36;2,56.50,621.11,231.89,9.36;2,56.50,633.11,231.89,9.36;2,56.50,645.11,23.83,9.36;2,80.32,642.96,7.37,6.21",
            ),
            Text(
                content="Self-reflective training on the spiritual dimensions within the students' own lives is recommended. 2",
                document_order=50,
                coordinates="2,90.92,645.11,197.48,9.36;2,56.51,657.11,227.44,9.36;2,283.94,654.96,3.69,6.21",
            ),
            Text(
                content="e developed a coherent set of realistic authentic learning tasks, in which students learn about and reflect on communication about the four dimensions of care, with a particular focus on the spiritual dimension.",
                document_order=51,
                coordinates="2,65.50,669.11,222.90,9.36;2,56.50,681.11,231.90,9.36;2,56.50,693.11,231.88,9.36;2,56.50,705.11,212.47,9.36",
            ),
            Text(
                content="The main aims of these learning tasks are that students learn about spiritual care, are able to talk about it with a palliative care patient, and to reflect on their spiritual experiences regarding life and death.",
                document_order=52,
                coordinates="2,271.54,705.11,16.86,9.36;2,56.50,717.11,231.88,9.36;2,56.50,729.11,231.90,9.36;2,306.89,45.11,231.90,9.36;2,306.89,57.11,157.54,9.36",
            ),
            Text(
                content="This article gives more insight into the usability and feasibility of these learning tasks from the stakeholders' perspectives, that is, medical students, teachers and educational scientists on the design of the learning tasks based on the educational principles of authentic educational scenarios, reflection and integration.",
                document_order=53,
                coordinates="2,467.16,57.11,71.62,9.36;2,306.89,69.11,231.90,9.36;2,306.89,81.11,231.88,9.36;2,306.89,93.11,231.89,9.36;2,306.89,105.11,231.89,9.36;2,306.89,117.11,231.90,9.36;2,306.89,129.11,115.41,9.36",
            ),
            Text(
                content="The research question is: How do medical students, teachers and educational scientists evaluate a set of coherent learning tasks focusing on the spiritual dimension of palliative care?",
                document_order=54,
                coordinates="2,426.79,129.11,112.00,9.36;2,306.89,141.11,231.89,9.36;2,306.89,153.11,231.90,9.36;2,306.89,165.11,228.96,9.36",
            ),
        ]
    ),
    Title(
        text=Text(
            content="METHODS",
            document_order=55,
            coordinates="2,306.89,189.29,47.13,9.24",
        )
    ),
    Title(
        text=Text(
            content="Design",
            document_order=56,
            coordinates="2,306.89,200.84,26.58,7.82",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="Three groups of stakeholders were asked to participate in this evaluation: medical students, teachers, and educational scientists.",
                document_order=57,
                coordinates="2,306.89,211.61,231.88,9.36;2,306.89,223.61,231.90,9.36;2,306.89,235.61,93.84,9.36",
            ),
            Text(
                content="The students were interviewed in focus groups.",
                document_order=58,
                coordinates="2,404.50,235.61,134.28,9.36;2,306.89,247.61,70.68,9.36",
            ),
            Text(
                content="The teachers and educational scientists were questioned in individual interviews, due to their busy schedules.",
                document_order=59,
                coordinates="2,381.54,247.61,157.23,9.36;2,306.89,259.61,231.89,9.36;2,306.89,271.61,92.69,9.36",
            ),
            Text(
                content="This qualitative approach was used to gather in-depth information and insights from our stakeholders.",
                document_order=60,
                coordinates="2,404.55,271.61,134.24,9.36;2,306.89,283.61,231.88,9.36;2,306.89,295.61,73.76,9.36",
            ),
        ]
    ),
    Title(
        text=Text(
            content="Setting",
            document_order=61,
            coordinates="2,306.89,319.34,27.97,7.82",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="In the Netherlands, it takes 6 years to qualify as a physician.",
                document_order=62,
                coordinates="2,306.89,330.11,231.88,9.36;2,306.89,342.11,20.24,9.36",
            ),
            Text(
                content="In the first 3 years, the Bachelor's program, the student primarily acquires theory and medical knowledge.",
                document_order=63,
                coordinates="2,330.85,342.11,207.93,9.36;2,306.89,354.11,231.89,9.36;2,306.89,366.11,22.54,9.36",
            ),
            Text(
                content="In the last 3 years, the Master's program, the focus is on the application of knowledge in the work setting by letting students rotate between different internships.",
                document_order=64,
                coordinates="2,334.14,366.11,204.63,9.36;2,306.89,378.11,231.90,9.36;2,306.89,390.11,231.88,9.36;2,306.89,402.11,49.79,9.36",
            ),
        ]
    ),
    Title(
        text=Text(
            content="Coherent set of learning tasks",
            document_order=65,
            coordinates="2,306.89,425.84,116.44,7.82",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="We designed a set of eight learning tasks (table 1; for a full description, see online supplemental appendix 1), designed to be integrated into the undergraduate medical curriculum.",
                document_order=66,
                coordinates="2,306.89,436.61,231.86,9.36;2,306.89,448.61,231.89,9.36;2,306.89,460.61,231.87,9.36;2,306.89,472.61,86.70,9.36",
            ),
            Text(
                content="The designers included diversity and variations in teaching methods, diseases, treatment plans, age and gender of the patient.",
                document_order=67,
                coordinates="2,397.51,472.61,141.26,9.36;2,306.89,484.61,231.89,9.36;2,306.89,496.61,178.30,9.36",
            ),
            Text(
                content="The competencies to be acquired are described in box 1.",
                document_order=68,
                coordinates="2,487.66,496.61,51.11,9.36;2,306.89,508.61,202.74,9.36",
            ),
            Text(
                content="These competences are a selection of the framework from Pieters et al. 19 The educational principles of authenticity, and reflection are incorporated into the set of learning tasks (see table 2).",
                document_order=69,
                coordinates="2,513.58,508.61,25.19,9.36;2,306.89,520.61,231.89,9.36;2,306.89,532.61,52.49,9.36;2,359.38,530.46,7.37,6.21;2,315.89,544.61,222.90,9.36;2,306.89,556.61,231.90,9.36;2,306.89,568.61,77.61,9.36",
            ),
        ]
    ),
    Title(
        text=Text(
            content="Original research",
            document_order=70,
            coordinates="3,448.91,24.52,85.87,9.48",
        )
    ),
    Title(
        text=Text(
            content="Participants",
            document_order=71,
            coordinates="3,56.50,225.44,36.35,7.82",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="Three groups of stakeholders were asked to participate in the evaluation: medical students, teachers and educational scientists.",
                document_order=72,
                coordinates="3,56.50,236.21,231.88,9.36;3,56.50,248.21,231.90,9.36;3,56.50,260.21,95.79,9.36",
            ),
            Text(
                content="The stakeholders came from faculties of medicine of four different universities in the Netherlands.",
                document_order=73,
                coordinates="3,158.01,260.21,130.37,9.36;3,56.50,272.21,231.88,9.36;3,56.50,284.21,71.47,9.36",
            ),
        ]
    ),
    Title(
        text=Text(
            content="Medical students (N=9)",
            document_order=74,
            coordinates="3,56.50,309.28,73.82,7.82",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="These stakeholders were asked to be interviewed in focus groups as they represented the educational users as learners.",
                document_order=75,
                coordinates="3,56.50,320.05,231.89,9.36;3,56.50,332.05,231.87,9.36;3,56.50,344.05,48.14,9.36",
            ),
            Text(
                content="Medical students in their final year of the Bachelor's program or studying for their Master's degree were invited.",
                document_order=76,
                coordinates="3,107.86,344.05,180.53,9.36;3,56.50,356.05,231.88,9.36;3,56.50,368.05,87.16,9.36",
            ),
            Text(
                content="These students have an informed opinion as to which tasks they deemed suitable for students and at what stage the tasks could best be implemented in the curriculum.",
                document_order=77,
                coordinates="3,146.62,368.05,141.78,9.36;3,56.50,380.05,231.87,9.36;3,56.50,392.05,231.90,9.36;3,56.50,404.05,135.74,9.36",
            ),
        ]
    ),
    Title(
        text=Text(
            content="Teachers of palliative care (N=9)",
            document_order=78,
            coordinates="3,56.50,429.12,101.30,7.82",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="These stakeholders were invited for their insight and experience in education and their substantive expertise in palliative care.",
                document_order=79,
                coordinates="3,56.50,439.89,231.87,9.36;3,56.50,451.89,231.88,9.36;3,56.50,463.89,73.68,9.36",
            ),
            Text(
                content="This group of stakeholders included medical specialists, mental healthcare providers and psychologists involved in teaching in undergraduate medical education.",
                document_order=80,
                coordinates="3,133.20,463.89,155.20,9.36;3,56.50,475.89,231.88,9.36;3,56.50,487.89,231.89,9.36;3,56.50,499.89,80.65,9.36",
            ),
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="Educational scientists (N=4)",
                document_order=81,
                coordinates="3,306.89,44.93,87.73,7.82",
            )
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="These stakeholders were asked for their expertise in both educational design and the educational principles used in this learning program (Authentic learning, reflection and integration into existing courses).",
                document_order=82,
                coordinates="3,306.89,55.70,231.90,9.36;3,306.89,67.70,231.90,9.36;3,306.89,79.70,231.89,9.36;3,306.89,91.70,211.09,9.36",
            ),
            Text(
                content="The educational scientists worked at medical faculties.",
                document_order=83,
                coordinates="3,521.90,91.70,16.86,9.36;3,306.89,103.70,212.67,9.36",
            ),
        ]
    ),
    Title(
        text=Text(
            content="Instruments",
            document_order=84,
            coordinates="3,306.89,129.24,46.29,7.82",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="The teachers and educational scientists were interviewed individually, the students were interviewed in focus groups, using the same semistructured interview guide (see online supplemental appendix 2).",
                document_order=85,
                coordinates="3,306.89,140.01,231.89,9.36;3,306.89,152.01,231.88,9.36;3,306.89,164.01,231.90,9.36;3,306.89,176.01,187.04,9.36",
            ),
            Text(
                content="The interview guide asked for perceptions of the set of learning tasks, focusing on the educational learning principles that shaped them: authentic learning tasks, the principles of reflective learning, and the integration into the existing courses.",
                document_order=86,
                coordinates="3,496.36,176.01,42.42,9.36;3,306.89,188.01,231.89,9.36;3,306.89,200.01,231.89,9.36;3,306.89,212.01,231.88,9.36;3,306.89,224.01,231.88,9.36;3,306.89,236.01,70.09,9.36",
            ),
        ]
    ),
    Title(
        text=Text(
            content="Procedure",
            document_order=87,
            coordinates="3,306.89,261.55,38.67,7.82",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="Participants were recruited through purposeful sampling within the network of Pasemeco until data saturation was reached.",
                document_order=88,
                coordinates="3,306.89,272.32,231.89,9.36;3,306.89,284.32,231.91,9.36;3,306.89,296.32,105.21,9.36",
            ),
            Text(
                content="They were invited through an email that included the information letter.",
                document_order=89,
                coordinates="3,417.20,296.32,121.57,9.36;3,306.89,308.32,195.27,9.36",
            ),
            Text(
                content="Prior to their individual or focus group interview, the participants received a short explanatory video and a document with an overview of the set of learning tasks.",
                document_order=90,
                coordinates="3,505.29,308.32,33.50,9.36;3,306.89,320.32,231.90,9.36;3,306.89,332.32,231.89,9.36;3,306.89,344.32,231.88,9.36",
            ),
            Text(
                content="The interviews took no more than 45 min and were conducted by JP and EN.",
                document_order=91,
                coordinates="3,306.89,356.32,231.90,9.36;3,306.89,368.32,109.85,9.36",
            ),
            Text(
                content="The interviewees gave their written informed consent.",
                document_order=92,
                coordinates="3,419.96,368.32,118.81,9.36;3,306.89,380.32,111.65,9.36",
            ),
        ]
    ),
    Title(
        text=Text(
            content="Analysis",
            document_order=93,
            coordinates="3,306.89,405.87,32.08,7.82",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="The interviews were recorded and transcribed.",
                document_order=94,
                coordinates="3,306.89,416.64,215.11,9.36",
            ),
            Text(
                content="To support the qualitative data analysis, Atlas.",
                document_order=95,
                coordinates="3,527.88,416.64,10.90,9.36;3,306.89,428.64,188.59,9.36",
            ),
            Text(
                content="ti V.8 was used.",
                document_order=96,
                coordinates="3,495.48,428.64,43.29,9.36;3,306.89,440.64,22.13,9.36",
            ),
            Text(
                content="The transcripts were analysed using template analysis, taking into account the step-by-step plan of Brooks et al. 26 Researchers JP, EN, and FW carried out the preliminary coding of the data, starting with determining the a priori themes.",
                document_order=97,
                coordinates="3,334.24,440.64,204.54,9.36;3,306.89,452.64,231.88,9.36;3,306.88,464.64,57.78,9.36;3,364.67,462.49,7.37,6.21;3,376.65,464.64,162.13,9.36;3,306.89,476.64,231.90,9.36;3,306.89,488.64,143.68,9.36",
            ),
            Text(
                content="These themes were based on the components of the research question (authentic learning tasks; reflection and integration into the curriculum).",
                document_order=98,
                coordinates="3,454.64,488.64,84.12,9.36;3,306.89,500.64,231.89,9.36;3,306.89,512.64,231.89,9.36;3,306.89,524.64,91.86,9.36",
            ),
            Text(
                content="Two interview transcripts were read and coded independently by researchers JP, EN, and FW.",
                document_order=99,
                coordinates="3,402.84,524.64,135.94,9.36;3,306.89,536.64,231.88,9.36;3,306.89,548.64,37.37,9.36",
            ),
            Text(
                content="They discussed their findings, merged the themes into meaningful clusters, and provided an initial coding template.",
                document_order=100,
                coordinates="3,349.37,548.64,189.39,9.36;3,306.89,560.64,231.90,9.36;3,306.89,572.64,98.00,9.36",
            ),
            Text(
                content="This template was then applied independently by the three researchers to three other transcripts.",
                document_order=101,
                coordinates="3,407.19,572.64,131.59,9.36;3,306.89,584.64,231.89,9.36;3,306.89,596.64,47.56,9.36",
            ),
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="After consultation, the template was finalised and applied to the full data set.",
                document_order=102,
                coordinates="3,315.89,608.64,222.88,9.36;3,306.89,620.64,124.20,9.36",
            ),
            Text(
                content="Themes were discussed and elaborated on iteratively with the whole research team.",
                document_order=103,
                coordinates="3,435.75,620.64,103.02,9.36;3,306.89,632.64,231.90,9.36;3,306.89,644.64,23.64,9.36",
            ),
            Text(
                content="JP and DV coded the other eight transcripts independently and discussed the results afterward.",
                document_order=104,
                coordinates="3,335.58,644.64,203.19,9.36;3,306.89,656.64,212.79,9.36",
            ),
            Text(
                content="The results were then discussed among all of the authors.",
                document_order=105,
                coordinates="3,521.92,656.64,16.86,9.36;3,306.89,668.64,225.50,9.36",
            ),
        ]
    ),
    Title(
        text=Text(
            content="Reflexivity",
            document_order=106,
            coordinates="3,306.89,694.18,41.27,7.82",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="This learning program was developed by a multidisciplinary group that included educational scientists (DV and DD), researchers (JP and EN) and physicians",
                document_order=107,
                coordinates="3,306.89,704.95,231.89,9.36;3,306.89,716.95,231.89,9.36;3,306.89,728.95,231.90,9.36",
            )
        ]
    ),
    Title(
        text=Text(
            content="Box 1: Intended competencies of the learning tasks",
            document_order=108,
            coordinates="3,62.50,50.89,200.31,9.48;3,62.50,62.39,21.66,9.48",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="Competencies:",
                document_order=109,
                coordinates="3,62.50,84.59,58.25,9.01",
            )
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="1) The student communicates in a respectful and empathetic manner with patients and relatives.",
                document_order=110,
                coordinates="3,62.50,95.59,216.64,9.01;3,62.50,106.59,127.30,9.01",
            )
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="2) The student makes the four dimensions (somatic, psychological, social and spiritual) of palliative care discussable with the patient and family.",
                document_order=111,
                coordinates="3,62.50,117.60,184.98,9.01;3,62.50,128.60,184.29,9.01;3,62.50,139.60,143.12,9.01",
            )
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="3) The student reflects on distance and closeness in the treatment relationship with a palliative patient.",
                document_order=112,
                coordinates="3,62.50,150.60,197.81,9.01;3,62.50,161.60,170.37,9.01",
            ),
            Text(
                content="4) The student reflects on his/her spiritual and existential views around life and death.",
                document_order=113,
                coordinates="3,62.50,172.60,203.60,9.01;3,62.50,183.60,102.51,9.01",
            ),
        ]
    ),
    Title(
        text=Text(
            content="RESULTS",
            document_order=114,
            coordinates="4,56.50,106.74,38.66,9.24",
        )
    ),
    Title(
        text=Text(
            content="Authentic tasks",
            document_order=115,
            coordinates="4,56.50,118.29,60.04,7.82",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="The stakeholders agreed that the educational materials, including the case descriptions, the video clips and short movies, showed the students a realistic view of what they could encounter in the workplace.",
                document_order=116,
                coordinates="4,56.50,129.06,231.90,9.36;4,56.50,141.06,231.90,9.36;4,56.50,153.06,231.88,9.36;4,56.50,165.06,231.90,9.36",
            ),
            Text(
                content="The learning tasks were authentic and presented in a logical and structured order, from paper cases to a fullfledged conversation with a patient.",
                document_order=117,
                coordinates="4,56.50,177.06,231.89,9.36;4,56.50,189.06,231.90,9.36;4,56.50,201.06,155.31,9.36",
            ),
            Text(
                content="The stakeholders commented that the learning tasks and materials could be further improved if they provided a better reflection of the cultural diversity within the patient population.",
                document_order=118,
                coordinates="4,215.03,201.06,73.37,9.36;4,56.50,213.06,231.90,9.36;4,56.50,225.06,231.89,9.36;4,56.50,237.06,231.90,9.36",
            ),
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="Students especially appreciated the clips in which real patients and doctors talked about palliative care and suggested that encouraging the possibility to discuss cases students have encountered in medical practice would further increase the authenticity.",
                document_order=119,
                coordinates="4,56.50,249.06,231.90,9.36;4,56.50,261.06,231.89,9.36;4,56.50,273.06,231.89,9.36;4,56.50,285.06,231.90,9.36;4,56.50,297.06,168.17,9.36",
            )
        ]
    ),
    Title(
        text=Text(
            content="Reflective learning",
            document_order=120,
            coordinates="4,56.50,322.24,72.59,7.82",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="Stakeholders recognised reflection is a recurring element across the learning tasks.",
                document_order=121,
                coordinates="4,56.50,333.01,231.88,9.36;4,56.50,345.01,141.35,9.36",
            ),
            Text(
                content="They also consider it to be an important skill.",
                document_order=122,
                coordinates="4,200.31,345.01,88.06,9.36;4,56.50,357.01,100.91,9.36",
            ),
            Text(
                content="According to the stakeholders, the majority of the students should be able to reflect well on the various health dimensions, but the spiritual dimension can be emotionally charged.",
                document_order=123,
                coordinates="4,159.63,357.01,128.75,9.36;4,56.50,369.01,231.90,9.36;4,56.50,381.01,231.90,9.36;4,56.50,393.01,174.42,9.36",
            ),
            Text(
                content="Some stakeholders indicated that to be able to reflect on this properly, some life experiences would not go amiss.",
                document_order=124,
                coordinates="4,235.46,393.01,52.94,9.36;4,56.50,405.01,231.89,9.36;4,56.50,417.01,198.88,9.36",
            ),
            Text(
                content="Novice medical students' reflections lack the necessary depth in comparison with Master's degree students.",
                document_order=125,
                coordinates="4,257.91,417.01,30.47,9.36;4,56.50,429.01,231.88,9.36;4,56.50,441.01,192.96,9.36",
            ),
            Text(
                content="Both the teachers and students preferred oral group reflection.",
                document_order=126,
                coordinates="4,251.93,441.01,36.47,9.36;4,56.50,453.01,231.88,9.36",
            ),
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="The students indicated that they attached great value to the interaction with their fellow students and that it helps them express themselves better.",
                document_order=127,
                coordinates="4,56.50,465.01,231.90,9.36;4,56.50,477.01,231.89,9.36;4,56.50,489.01,168.94,9.36",
            ),
            Text(
                content="Student safety must be ensured in order for them to properly reflect in a group.",
                document_order=128,
                coordinates="4,228.24,489.01,60.14,9.36;4,56.50,501.01,231.88,9.36;4,56.50,513.01,46.77,9.36",
            ),
        ]
    ),
    Title(
        text=Text(
            content="Integration",
            document_order=129,
            coordinates="4,56.50,538.19,43.55,7.82",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="The stakeholders believed that the learning tasks should be integrated across the curriculum in different years.",
                document_order=130,
                coordinates="4,56.50,548.96,231.88,9.36;4,56.50,560.96,231.88,9.36",
            ),
            Text(
                content="However, it is important that this does not become too fragmented and that students can clearly see the cohesion.",
                document_order=131,
                coordinates="4,56.50,572.96,231.89,9.36;4,56.50,584.96,231.89,9.36;4,56.50,596.96,20.38,9.36",
            ),
            Text(
                content="Almost all stakeholders mentioned that the initial tasks (tasks 1-5) would be best implemented in the Bachelor's program, as the cases in these tasks revolve around the basis of palliative care.",
                document_order=132,
                coordinates="4,79.30,596.96,209.08,9.36;4,56.50,608.96,231.91,9.36;4,56.50,620.96,231.89,9.36;4,56.50,632.96,148.00,9.36",
            ),
            Text(
                content="The other learning tasks (tasks 6-8) were considered more appropriate for more advanced students during the internships as these center around communication with a simulated or real patient.",
                document_order=133,
                coordinates="4,207.59,632.96,80.81,9.36;4,56.50,644.96,231.89,9.36;4,56.50,656.96,231.89,9.36;4,56.50,668.96,231.88,9.36;4,56.50,680.96,92.17,9.36",
            ),
            Text(
                content="According to the stakeholders, they required experience with patients that students only acquire during the Master's degree.",
                document_order=134,
                coordinates="4,153.08,680.96,135.29,9.36;4,56.50,692.96,231.88,9.36;4,56.50,704.96,181.77,9.36",
            ),
            Text(
                content="There was no consensus as to when to start the learning trajectory.",
                document_order=135,
                coordinates="4,242.68,704.96,45.72,9.36;4,56.50,716.96,231.90,9.36;4,56.50,728.96,19.29,9.36",
            ),
            Text(
                content="Some stakeholders believed that palliative care education should start in the very first year, so that students become immediately aware that palliative care is a part of routine care.",
                document_order=136,
                coordinates="4,80.35,728.96,208.04,9.36;4,306.89,45.11,231.89,9.36;4,306.89,57.11,231.90,9.36;4,306.89,69.11,133.09,9.36",
            ),
            Text(
                content="But others thought it better to wait until the end of the Bachelor's program, because students would not be open to the subject or not fully understand the subject matter until then.",
                document_order=137,
                coordinates="4,444.37,69.11,94.41,9.36;4,306.89,81.11,231.89,9.36;4,306.89,93.11,231.89,9.36;4,306.89,105.11,213.52,9.36",
            ),
            Text(
                content="The implementation should also take into account the differences between students.",
                document_order=138,
                coordinates="4,315.89,117.11,222.89,9.36;4,306.89,129.11,142.94,9.36",
            ),
            Text(
                content="In the final learning task, students conduct an unsupervised interview with a palliative patient.",
                document_order=139,
                coordinates="4,452.97,129.11,85.81,9.36;4,306.89,141.11,231.89,9.36;4,306.89,153.11,81.89,9.36",
            ),
            Text(
                content="According to the stakeholders, the learning program does prepare students well for this interview, but it is still an emotionally charged task.",
                document_order=140,
                coordinates="4,391.67,153.11,147.11,9.36;4,306.89,165.11,231.88,9.36;4,306.89,177.11,231.90,9.36",
            ),
            Text(
                content="In order to protect both the patients and the students, the students must be well prepared and be able to take the lead in such an interview.",
                document_order=141,
                coordinates="4,306.89,189.11,231.89,9.36;4,306.89,201.11,231.90,9.36;4,306.89,213.11,124.16,9.36",
            ),
            Text(
                content="Some students may need more training or support (table 3).",
                document_order=142,
                coordinates="4,433.77,213.11,105.03,9.36;4,306.89,225.11,147.84,9.36",
            ),
        ]
    ),
    Title(
        text=Text(
            content="DISCUSSION",
            document_order=143,
            coordinates="4,306.89,249.29,56.35,9.24",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="The medical students, teachers, and educational scientists agree that the set of learning tasks was designed in line with contemporary instructional design guidelines.",
                document_order=144,
                coordinates="4,306.89,261.11,231.89,9.36;4,306.89,273.11,231.90,9.36;4,306.89,285.11,231.89,9.36;4,306.89,297.11,22.23,9.36",
            ),
            Text(
                content="Learning was clearly organised around authentic learning tasks relevant to the later profession, using paper, video cases, as well as simulations and real patients.",
                document_order=145,
                coordinates="4,331.78,297.11,207.01,9.36;4,306.89,309.11,231.89,9.36;4,306.89,321.11,231.89,9.36;4,306.89,333.11,36.27,9.36",
            ),
            Text(
                content="The tasks encourage the students to reflect on the four dimensions of palliative care and their personal values.",
                document_order=146,
                coordinates="4,347.41,333.11,191.36,9.36;4,306.89,345.11,231.88,9.36;4,306.89,357.11,69.73,9.36",
            ),
            Text(
                content="There were various options offered for the integration of the tasks into existing curricula.",
                document_order=147,
                coordinates="4,381.04,357.11,157.74,9.36;4,306.89,369.11,231.87,9.36",
            ),
            Text(
                content="The stakeholders also offered a number of suggestions to take into account, which will be discussed further.",
                document_order=148,
                coordinates="4,306.89,381.11,231.90,9.36;4,306.89,393.11,225.88,9.36",
            ),
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="First, palliative care and the spiritual dimension in particular are emotionally charged subjects.",
                document_order=149,
                coordinates="4,315.89,405.11,222.88,9.36;4,306.89,417.11,204.25,9.36",
            ),
            Text(
                content="Extra attention to both student and patient safety is required.",
                document_order=150,
                coordinates="4,515.34,417.11,23.44,9.36;4,306.89,429.11,231.88,9.36",
            ),
            Text(
                content="Both the students and teachers attached great value to the group discussions and reflections, where a bond of trust and psychological safety between all of the attendees was considered to be essential.",
                document_order=151,
                coordinates="4,306.89,441.11,231.88,9.36;4,306.89,453.11,231.87,9.36;4,306.89,465.11,231.87,9.36;4,306.89,477.11,178.53,9.36",
            ),
            Text(
                content="These findings are in line with the literature, where confidentially sharing experiences is needed and only possible in a group of people who know each other. 2 27 Second, the educational materials were considered authentic with variation in cases and learning methods, but to increase authenticity, the stakeholders suggested including more cultural diversity among the patient cases used in the learning tasks.",
                document_order=152,
                coordinates="4,489.22,477.11,49.57,9.36;4,306.89,489.11,231.90,9.36;4,306.89,501.11,231.90,9.36;4,306.89,513.11,166.83,9.36;4,473.72,510.96,12.90,6.21;4,315.89,525.11,222.88,9.36;4,306.89,537.11,231.89,9.36;4,306.89,549.11,231.89,9.36;4,306.89,561.11,231.89,9.36;4,306.89,573.11,134.15,9.36",
            ),
            Text(
                content="Contemporary society is more culturally diverse than the current materials reflected.",
                document_order=153,
                coordinates="4,443.75,573.11,95.04,9.36;4,306.89,585.11,231.90,9.36;4,306.89,597.11,39.97,9.36",
            ),
            Text(
                content="It is an important topic that should not be overlooked, given that many physicians are unfamiliar with the specific needs of ethnic minorities regarding palliative care and communication. 28",
                document_order=154,
                coordinates="4,350.66,597.11,188.12,9.36;4,306.89,609.11,231.90,9.36;4,306.89,621.11,231.88,9.36;4,306.89,633.11,150.06,9.36;4,456.93,630.96,7.37,6.21",
            ),
            Text(
                content="hird, there was discussion on how to integrate learning tasks or palliative care education in general.",
                document_order=155,
                coordinates="4,315.89,645.11,222.89,9.36;4,306.89,657.11,231.89,9.36",
            ),
            Text(
                content="All participants agreed that this should start in the Bachelors and most agreed that it should be integrated vertically, throughout the undergraduate program and not as a stand-alone module.",
                document_order=156,
                coordinates="4,306.89,669.11,231.89,9.36;4,306.89,681.11,231.90,9.36;4,306.89,693.11,231.87,9.36;4,306.89,705.11,156.93,9.36",
            ),
            Text(
                content="Furthermore, it needs to be integrated horizontally, where relevant, for instance, in cardiology, oncology, humanities, and copyright.",
                document_order=157,
                coordinates="4,469.68,705.11,69.11,9.36;4,306.89,717.11,231.90,9.36;4,306.89,729.11,231.89,9.36;4,567.14,376.44,8.32,39.01",
            ),
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="on January 21, 2022 by guest.",
                document_order=158,
                coordinates="4,576.14,582.02,8.33,10.01;4,576.14,594.53,8.33,32.01;4,576.14,629.05,8.32,12.51;4,576.14,644.06,8.33,20.02;4,576.14,666.58,8.33,9.50;4,576.14,678.58,8.33,24.52",
            ),
            Text(
                content="Protected by http://spcare.bmj.com/",
                document_order=159,
                coordinates="4,576.14,705.60,8.33,38.52;4,576.14,746.62,8.33,9.50;4,576.14,490.99,8.33,88.53",
            ),
            Text(
                content="Original research communication training.",
                document_order=160,
                coordinates="5,448.91,24.52,85.87,9.48;5,56.50,512.98,104.79,9.36",
            ),
            Text(
                content="Integrating this set of learning tasks, therefore, mainly depends on the curriculum of a medical university and its identity as to where and when palliative care education can be implemented in the curriculum.",
                document_order=161,
                coordinates="5,163.19,512.98,125.21,9.36;5,56.50,524.98,231.88,9.36;5,56.50,536.98,231.90,9.36;5,56.50,548.98,231.90,9.36;5,56.50,560.98,65.80,9.36",
            ),
            Text(
                content="The idea of vertically and horizontally integration is in line with recent educational research and guidelines. 4 29 30",
                document_order=162,
                coordinates="5,124.97,560.98,163.40,9.36;5,56.50,572.98,231.89,9.36;5,56.50,584.98,64.18,9.36;5,120.67,582.83,22.12,6.21",
            ),
            Text(
                content="ome stakeholders argued that for learning about spiritual and palliative care in general, students should have some life experience and, therefore, it would be more suitable to start the program later in the bachelor.",
                document_order=163,
                coordinates="5,65.50,596.98,222.90,9.36;5,56.50,608.98,231.89,9.36;5,56.50,620.98,231.89,9.36;5,56.50,632.98,231.90,9.36",
            ),
            Text(
                content="Others argue that palliative care should be normalised for the students and should, therefore, start in the first year.",
                document_order=164,
                coordinates="5,56.50,644.98,231.89,9.36;5,56.50,656.98,231.89,9.36;5,56.50,668.98,20.34,9.36",
            ),
            Text(
                content="The concern that early exposure may be emotionally challenging for young students, is the main reason why curricula integrate palliative care education in general later in the program. 31 32",
                document_order=165,
                coordinates="5,79.00,668.98,209.39,9.36;5,56.50,680.98,231.89,9.36;5,56.50,692.98,231.89,9.36;5,56.50,704.98,128.64,9.36;5,185.13,702.83,17.54,6.21",
            ),
            Text(
                content="However, research shows that direct experience with palliative care for first-year students is associated with positive effects on the students' attitudes regarding caring for palliative care patients. 29 31 33 34",
                document_order=166,
                coordinates="5,206.90,704.98,81.49,9.36;5,56.50,716.98,231.89,9.36;5,56.50,728.98,231.87,9.36;5,306.89,512.98,231.91,9.36;5,306.89,524.98,56.36,9.36;5,363.24,522.83,34.36,6.21",
            ),
            Text(
                content="Junior doctors who were trained earlier in palliative care have enhanced competencies of psychosocial and spiritual aspects of palliative care, communication, and self-awareness. 34",
                document_order=167,
                coordinates="5,400.07,524.98,138.71,9.36;5,306.89,536.98,231.89,9.36;5,306.89,548.98,231.90,9.36;5,306.89,560.98,164.04,9.36;5,470.92,558.83,7.37,6.21",
            ),
            Text(
                content="Thus, early exposure helps to normalise death and dying and the complex emotions that students and physicians can encounter while treating palliative care patients. 31 33 34",
                document_order=168,
                coordinates="5,486.00,560.98,52.77,9.36;5,306.88,572.98,231.89,9.36;5,306.88,584.98,231.89,9.36;5,306.88,596.98,206.08,9.36;5,512.96,594.83,25.81,6.21",
            ),
            Text(
                content="nterestingly, in this study, students themselves had lively discussions on this topic too, but they mainly discussed more practical obstacles: when is there time for this in the curriculum?",
                document_order=169,
                coordinates="5,306.89,608.98,231.89,9.36;5,306.89,620.98,231.88,9.36;5,306.89,632.98,231.87,9.36;5,306.89,644.98,112.32,9.36",
            ),
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="This study had some limitations.",
                document_order=170,
                coordinates="5,315.89,656.98,141.26,9.36",
            ),
            Text(
                content="To begin with, we evaluated the set of learning tasks prior to its implementation.",
                document_order=171,
                coordinates="5,460.51,656.98,78.29,9.36;5,306.89,668.98,231.88,9.36;5,306.89,680.98,46.39,9.36",
            ),
            Text(
                content="This meant that we could not reflect on the implementation process itself, leaving this to be researched at a later stage.",
                document_order=172,
                coordinates="5,357.66,680.98,181.12,9.36;5,306.89,692.98,231.89,9.36;5,306.89,704.98,137.26,9.36",
            ),
            Text(
                content="We also focused on the stakeholders in the educational setting: medical students, teachers, and educational scientists.",
                document_order=173,
                coordinates="5,449.30,704.98,89.46,9.36;5,306.89,716.98,231.89,9.36;5,306.89,728.98,195.29,9.36",
            ),
            Text(
                content="Patients'I would also pay more attention to a more diversified background,(…).",
                document_order=174,
                coordinates="5,505.64,728.98,33.14,9.36;5,108.50,156.07,221.01,8.06",
            ),
            Text(
                content="The impression here is that it might be more about the classic white Dutch native than perhaps the Surinamese or Moroccan who gets into these problems and needs an essentially different approach'-I7",
                document_order=175,
                coordinates="5,330.77,156.07,189.69,8.06;5,108.50,165.57,422.62,8.06;5,108.50,175.07,12.26,8.06",
            ),
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="'(the clips, eds.)in the sense that the doctors who were talking, for example a [person] I have met in the clinic as well so that appeals more to the imagination.",
                document_order=176,
                coordinates="5,108.50,203.57,426.67,8.06;5,108.50,213.08,59.04,8.06",
            ),
            Text(
                content="That actually makes it even more authentic'-FG2",
                document_order=177,
                coordinates="5,168.80,213.08,153.12,8.06",
            ),
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="'That there are not only videos but also something like a link to a wishlist, and a Volkskrant [newspaper] article so I think that's already very authentic.",
                document_order=178,
                coordinates="5,108.50,241.58,429.85,8.06;5,108.50,251.08,30.85,8.06",
            ),
            Text(
                content="You might want to make it a little more authentic by having students contribute cases they encounter'-FG2 Reflective learning'I believe, indeed, that in real life that might be better than on paper, especially because you sometimes have to put something on paper and then you are not really sure or you feel differently or have not enough time and if you are really working in such a group, then ideas emerge or feelings that other people then evoke in you or you hear it and you think, oh that's right, I agree or I do not'-FG1'What is also important here is that in your educational groups, or in the subgroup where you would discuss this, you have a bond of trust as well as feel safe'-I11",
                document_order=179,
                coordinates="5,140.60,251.08,334.78,8.06;5,60.50,263.46,29.61,8.06;5,60.50,272.96,25.03,8.06;5,108.50,263.46,419.16,8.06;5,108.50,272.96,418.97,8.06;5,108.50,282.46,386.39,8.06;5,108.50,310.96,424.83,8.06;5,108.50,320.47,76.74,8.06",
            ),
        ]
    ),
    Title(
        text=Text(
            content="Integration",
            document_order=180,
            coordinates="5,60.50,332.84,33.70,8.06",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="And what might also be good timing,(…), is the second half of the third year of medicine.",
                document_order=181,
                coordinates="5,108.50,332.84,277.17,8.06",
            ),
            Text(
                content="Students are then very receptive to everything that is useful in their internships, so to speak, because then it is kind of a big thing that you will have to tackle soon and so you have to get started'-FG2",
                document_order=182,
                coordinates="5,387.39,332.84,141.06,8.06;5,108.50,342.35,429.36,8.06;5,108.50,351.85,44.36,8.06",
            ),
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="'I see no reason not to do it (integration as of year 1, eds.).",
                document_order=183,
                coordinates="5,108.50,380.35,181.60,8.06",
            ),
            Text(
                content="And another advantage is that students will get an idea of-oh, yes, so this is part of the job as well?",
                document_order=184,
                coordinates="5,291.36,380.35,238.27,8.06;5,108.50,389.85,71.45,8.06",
            ),
            Text(
                content="It soon makes it more normal, because students often enrol with a strong idea of: we are going to make everyone better… but accepting that you can't make someone better will become the reality… but it is not really part of the idea of beginning students so, in that sense, I think: maybe it's also good to create some kind of awareness here'-I12",
                document_order=185,
                coordinates="5,181.99,389.85,349.34,8.06;5,108.50,399.35,409.56,8.06;5,108.50,408.86,305.78,8.06",
            ),
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="'I believe you could use that simulation interview as a go/no-go for having an interview with a patient.",
                document_order=186,
                coordinates="5,108.50,437.36,316.08,8.06",
            ),
            Text(
                content="And, once again, they really are vulnerable patients, often in the final stage of life, who are often quite willing to contribute to the training, but who should also not be burdened disproportionately by oafs or students who are not interested or cut corners, and that such a patient is about to go home with a bad feeling after 45 minutes'-I8 FG, Focus Group; I, Interview.",
                document_order=187,
                coordinates="5,425.84,437.36,97.24,8.06;5,108.50,446.86,414.15,8.06;5,108.50,456.36,425.00,8.06;5,108.50,465.87,102.09,8.06;5,60.50,478.19,90.18,8.06",
            ),
            Text(
                content="were not involved in the evaluation, although they were involved in the overarching project within which the learning tasks were developed.",
                document_order=188,
                coordinates="6,56.50,45.11,231.87,9.36;6,56.50,57.12,231.87,9.36;6,56.50,69.13,150.15,9.36",
            ),
            Text(
                content="Last but not least, the educational principles within this learning program were tailored to the Dutch situation.",
                document_order=189,
                coordinates="6,210.12,69.13,78.29,9.36;6,56.50,81.14,231.87,9.36;6,56.50,93.15,159.03,9.36",
            ),
            Text(
                content="The educational principles and general setup of the design are internationally transferable, if tailored to the national situation.",
                document_order=190,
                coordinates="6,218.82,93.15,69.57,9.36;6,56.50,105.16,231.89,9.36;6,56.50,117.17,231.90,9.36;6,56.50,129.18,39.88,9.36",
            ),
            Text(
                content="Following the authenticity principle means that it is important to paint a realistic picture of the professional field.",
                document_order=191,
                coordinates="6,100.44,129.18,187.95,9.36;6,56.50,141.19,231.90,9.36;6,56.50,153.20,77.26,9.36",
            ),
            Text(
                content="If authenticity is to be guaranteed, learning tasks will have to be reviewed and adapted to be used in other countries.",
                document_order=192,
                coordinates="6,137.41,153.20,150.97,9.36;6,56.50,165.21,231.89,9.36;6,56.50,177.22,127.15,9.36",
            ),
            Text(
                content="This also regards to the principle of reflective learning.",
                document_order=193,
                coordinates="6,186.79,177.22,101.60,9.36;6,56.50,189.23,133.47,9.36",
            ),
            Text(
                content="The students involved in this study are already familiar with reflecting and sharing their opinion, since it plays a vital role in their curriculum.",
                document_order=194,
                coordinates="6,193.19,189.23,95.19,9.36;6,56.50,201.24,231.89,9.36;6,56.50,213.25,231.88,9.36;6,56.50,225.26,49.64,9.36",
            ),
            Text(
                content="On a national level there is a lively debate on end-of-life care, but not on the spiritual dimension.",
                document_order=195,
                coordinates="6,108.94,225.26,179.46,9.36;6,56.50,237.27,231.89,9.36",
            ),
            Text(
                content="Therefore, an emphasis was placed on the spiritual dimension.",
                document_order=196,
                coordinates="6,56.51,249.28,231.88,9.36;6,56.51,261.29,47.17,9.36",
            ),
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="This study has several practical implications.",
                document_order=197,
                coordinates="6,65.51,273.30,196.78,9.36",
            ),
            Text(
                content="First, it pays off to integrate the program horizontally and vertically into the curriculum.",
                document_order=198,
                coordinates="6,266.39,273.30,22.01,9.36;6,56.51,285.31,231.87,9.36;6,56.51,297.32,160.16,9.36",
            ),
            Text(
                content="It depends on the specific tasks and the curriculum itself how and where the integration can best take place.",
                document_order=199,
                coordinates="6,222.91,297.32,65.48,9.36;6,56.51,309.33,231.90,9.36;6,56.51,321.34,181.09,9.36",
            ),
            Text(
                content="Some tasks will fit in well with education regarding communication or where clinical conditions are discussed such as oncology or lung disease.",
                document_order=200,
                coordinates="6,240.93,321.34,47.47,9.36;6,56.51,333.35,231.90,9.36;6,56.51,345.36,231.87,9.36;6,56.51,357.37,109.08,9.36",
            ),
            Text(
                content="To avoid fragmentation and guarantee that all aspects are covered, however, it is also important that someone has an overview of where and how palliative care is addressed in the curriculum, for example, a curriculum coordinator or someone specifically assigned with this task.",
                document_order=201,
                coordinates="6,168.62,357.37,119.77,9.36;6,56.51,369.38,231.90,9.36;6,56.51,381.39,231.88,9.36;6,56.51,393.40,231.89,9.36;6,56.51,405.41,231.88,9.36;6,56.51,417.42,153.03,9.36",
            ),
            Text(
                content="Furthermore, the tasks can always be adapted to specific contexts.",
                document_order=202,
                coordinates="6,213.64,417.42,74.76,9.36;6,56.51,429.43,213.40,9.36",
            ),
            Text(
                content="For example, it might be difficult to arrange interviews with palliative care patients.",
                document_order=203,
                coordinates="6,273.72,429.43,14.69,9.36;6,56.51,441.44,231.89,9.36;6,56.51,453.45,119.44,9.36",
            ),
            Text(
                content="Students could then interview a chronically ill patient instead of a palliative patient.",
                document_order=204,
                coordinates="6,178.45,453.45,109.95,9.36;6,56.51,465.46,231.90,9.36;6,56.51,477.47,32.57,9.36",
            ),
            Text(
                content="With explicit attention to communication and spiritual care education, it is possible to better prepare students for working in the professional field.",
                document_order=205,
                coordinates="6,91.84,477.47,196.56,9.36;6,56.51,489.48,231.88,9.36;6,56.51,501.49,209.89,9.36",
            ),
            Text(
                content="The spiritual dimension of care deserves explicit attention in the medical curriculum.",
                document_order=206,
                coordinates="6,271.55,501.49,16.86,9.36;6,56.51,513.50,231.89,9.36;6,56.51,525.51,112.93,9.36",
            ),
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content=", 2022 by guest.",
                document_order=207,
                coordinates="5,581.69,629.05,2.77,12.51;5,576.14,644.06,8.33,20.02;5,576.14,666.58,8.33,9.50;5,576.14,678.58,8.33,24.52",
            ),
            Text(
                content="Protected by http://spcare.bmj.com/",
                document_order=208,
                coordinates="5,576.14,705.60,8.33,38.52;5,576.14,746.62,8.33,9.50;5,576.14,490.99,8.33,88.53",
            ),
            Text(
                content="Original research",
                document_order=209,
                coordinates="6,60.50,24.52,85.87,9.48",
            ),
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="The eight learning tasks",
                document_order=210,
                coordinates="2,348.73,604.84,81.98,9.01",
            )
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="The incorporated educational principles in the different learning tasks",
                document_order=211,
                coordinates="3,98.34,541.72,188.43,9.01;3,60.50,552.72,47.85,9.01",
            )
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="Themes and quotes of the stakeholders this(authenticity, eds.)in so far that patients tell you a lot of stories.",
                document_order=212,
                coordinates="5,98.34,50.36,134.78,9.01;5,145.80,80.06,206.18,8.06",
            ),
            Text(
                content="So, in that sense, they are all very authentic stories and this is how patients present themselves to doctors'-I10'If you look at the learning tasks, you do see a clear structure.",
                document_order=213,
                coordinates="5,353.71,80.06,182.09,8.06;5,108.50,89.56,161.34,8.06;5,108.50,118.06,189.47,8.06",
            ),
            Text(
                content="From watching to an increasingly active role to eventually actually having a conversation with a patient, of course'-I8",
                document_order=214,
                coordinates="5,299.70,118.06,231.07,8.06;5,108.50,127.57,130.78,8.06",
            ),
        ]
    ),
    Meta(meta_type="acknowledgements_start"),
    Title(
        text=Text(
            content="Acknowledgements",
            document_order=215,
            coordinates="6,56.50,548.07,69.90,8.06",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="We thank Judith Westen and Jimmy Frerejean for their support in designing these learning tasks.",
                document_order=216,
                coordinates="6,130.65,548.07,129.88,7.96;6,56.50,557.58,218.13,7.96",
            ),
            Text(
                content="We further thank the involved students, teachers and educational scientist.",
                document_order=217,
                coordinates="6,276.96,557.58,11.43,7.96;6,56.50,567.09,222.78,7.96;6,56.50,576.60,31.41,7.96",
            ),
        ]
    ),
    Meta(meta_type="acknowledgements_end"),
    Meta(meta_type="annex_start"),
    Paragraph(
        sentences=[
            Text(
                content="Contributors DV and FW developed the learning tasks; JP and EN conducted the data collection.",
                document_order=218,
                coordinates="6,56.50,590.11,227.18,8.07;6,56.50,599.62,124.24,7.96",
            ),
            Text(
                content="JP, EN and FW interpreted the data.",
                document_order=219,
                coordinates="6,183.11,599.62,97.60,7.96;6,56.50,609.13,31.66,7.96",
            ),
            Text(
                content="JP drafted the manuscript; DV, MvdBvE and DD.",
                document_order=220,
                coordinates="6,90.53,609.13,179.27,7.96",
            ),
            Text(
                content="supervised the study process.",
                document_order=221,
                coordinates="6,56.50,618.64,105.25,7.96",
            ),
            Text(
                content="All authors have read and agreed to the final version of the manuscript.",
                document_order=222,
                coordinates="6,164.11,618.64,119.80,7.96;6,56.50,628.15,137.67,7.96",
            ),
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="Funding This work was supported by ZonMW (project number 80-84400-98-027).",
                document_order=223,
                coordinates="6,56.50,641.66,231.68,8.07;6,56.50,651.17,70.40,7.96",
            )
        ]
    ),
    Title(
        text=Text(
            content="Competing interests None declared.",
            document_order=224,
            coordinates="6,56.50,664.68,132.07,8.07",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="Patient consent for publication Not required.",
                document_order=225,
                coordinates="6,56.50,678.18,164.07,8.07",
            )
        ]
    ),
    Title(
        text=Text(
            content="Ethics approval Ethical clearance was obtained from the Netherlands Association for Medical Education Ethical Review",
            document_order=226,
            coordinates="6,56.50,691.69,204.20,8.07;6,56.50,701.20,229.14,7.96",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="Board (NVMO-ERB file 2020.5.3).",
                document_order=227,
                coordinates="6,56.50,710.71,128.95,7.96",
            ),
            Text(
                content="Written consent was obtained from all participants.",
                document_order=228,
                coordinates="6,187.82,710.71,73.58,7.96;6,56.50,720.23,110.46,7.96",
            ),
            Text(
                content="The participants gave their permission to use anonymised quotes.",
                document_order=229,
                coordinates="6,169.32,720.23,97.51,7.96;6,56.50,729.74,137.92,7.96",
            ),
        ]
    ),
    Paragraph(
        sentences=[
            Text(
                content="Provenance and peer review Not commissioned; externally peer reviewed.",
                document_order=230,
                coordinates="6,306.88,45.02,215.24,8.07;6,306.88,54.66,53.42,7.96",
            )
        ]
    ),
    Title(
        text=Text(
            content="Data availability statement Data are available on reasonable request.",
            document_order=231,
            coordinates="6,306.88,68.30,218.74,8.07;6,306.88,77.94,28.76,7.96",
        )
    ),
    Title(
        text=Text(
            content="Open access This is an open access article distributed in accordance with the Creative Commons Attribution Non",
            document_order=232,
            coordinates="6,306.88,91.08,203.26,8.07;6,306.88,100.22,207.66,7.96",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="Commercial (CC BY-NC 4.0) license, which permits others to distribute, remix, adapt, build upon this work noncommercially, and license their derivative works on different terms, provided the original work is properly cited, appropriate credit is given, any changes made indicated, and the use is noncommercial.",
                document_order=233,
                coordinates="6,306.88,109.36,214.63,7.96;6,306.88,118.49,195.94,7.96;6,306.88,127.63,220.30,7.96;6,306.88,136.77,231.89,7.96;6,306.88,145.91,230.06,7.96;6,306.88,155.04,44.63,7.96",
            ),
            Text(
                content="See: http:// creativecommons.",
                document_order=234,
                coordinates="6,353.87,155.04,105.68,7.96",
            ),
            Text(
                content="org/ licenses/ by-nc/ 4. 0/.",
                document_order=235,
                coordinates="6,459.54,155.04,73.63,7.96;6,306.88,164.18,9.45,7.96",
            ),
        ]
    ),
    Title(
        text=Text(
            content="ORCID iD",
            document_order=236,
            coordinates="6,306.88,181.82,39.98,8.06",
        )
    ),
    Paragraph(
        sentences=[
            Text(
                content="Jolien Pieters http:// orcid.",
                document_order=237,
                coordinates="6,306.88,191.46,94.21,7.96",
            ),
            Text(
                content="org/ 0000-0002-9327-3977",
                document_order=238,
                coordinates="6,401.10,191.46,98.73,7.96",
            ),
        ]
    ),
    Meta(meta_type="annex_end"),
]
sentences = [
    Text(
        content="Background Palliative care is gaining importance within the physician's range of duties.",
        document_order=0,
        coordinates="1,166.78,241.37,137.11,8.06;1,166.78,253.96,153.49,8.06;1,166.78,266.56,24.09,8.06",
    ),
    Text(
        content="In the undergraduate medical curriculum, education on the four dimensions of care is insufficient.",
        document_order=1,
        coordinates="1,193.23,266.56,150.18,8.06;1,166.78,279.16,157.13,8.06;1,166.78,291.76,41.88,8.06",
    ),
    Text(
        content="The spiritual dimension is hardly addressed.",
        document_order=2,
        coordinates="1,211.02,291.76,115.56,8.06;1,166.78,304.35,38.58,8.06",
    ),
    Text(
        content="Therefore, we developed a coherent set of learning tasks targeted at learning to communicate about the spiritual dimension.",
        document_order=3,
        coordinates="1,207.72,304.35,130.84,8.06;1,166.78,316.95,156.63,8.06;1,166.78,329.55,159.63,8.06",
    ),
    Text(
        content="The learning tasks are based on educational principles of authentic learning, reflective learning and longitudinal integration in the curriculum.",
        document_order=4,
        coordinates="1,166.78,342.14,158.70,8.06;1,166.78,354.74,149.23,8.06;1,166.78,367.34,156.03,8.06;1,166.78,379.93,40.60,8.06",
    ),
    Text(
        content="This article reports on the feasibility of using these learning tasks in the medical curricula.",
        document_order=5,
        coordinates="1,209.74,379.93,127.81,8.06;1,166.78,392.53,156.48,8.06;1,166.78,405.13,33.05,8.06",
    ),
    Text(
        content="Methods Teachers and educational scientists were interviewed and students were asked to evaluate the learning tasks in focus groups.",
        document_order=6,
        coordinates="1,166.78,417.73,165.28,8.06;1,166.78,430.32,164.53,8.06;1,166.78,442.92,156.81,8.06",
    ),
    Text(
        content="Interview transcripts were analysed by three independent researchers.",
        document_order=7,
        coordinates="1,166.78,455.52,158.35,8.06;1,166.78,468.11,90.85,8.06",
    ),
    Text(
        content="The learning tasks encourage the students to reflect on the four dimensions of palliative care and their personal values.",
        document_order=9,
        coordinates="1,199.36,480.71,120.12,8.06;1,166.78,493.31,161.86,8.06;1,166.78,505.90,143.88,8.06",
    ),
    Text(
        content="Learning was clearly organised around authentic learning tasks relevant to the later profession, using paper, video cases, as well as simulations and real patients.",
        document_order=10,
        coordinates="1,313.02,505.90,31.32,8.06;1,166.78,518.50,173.33,8.06;1,166.78,531.10,155.07,8.06;1,166.78,543.70,163.58,8.06;1,166.78,556.29,46.60,8.06",
    ),
    Text(
        content="Participants suggest giving more attention to cultural diversity.",
        document_order=11,
        coordinates="1,215.74,556.29,116.97,8.06;1,166.78,568.89,105.46,8.06",
    ),
    Text(
        content="As palliative care is an emotionally charged subject, the safety of both student and patient should be guaranteed.",
        document_order=12,
        coordinates="1,274.60,568.89,60.28,8.06;1,166.78,581.49,170.48,8.06;1,166.78,594.08,174.79,8.06",
    ),
    Text(
        content="All participants indicated that the program should start in the bachelor phase and most agreed that it should be integrated vertically and horizontally throughout the undergraduate program, although there is some debate about the optimal moment to start.",
        document_order=13,
        coordinates="1,166.78,606.68,153.80,8.06;1,166.78,619.28,159.18,8.06;1,166.78,631.87,159.94,8.06;1,166.78,644.47,172.25,8.06;1,166.78,657.07,169.74,8.06;1,166.78,669.67,105.31,8.06",
    ),
    Text(
        content="Conclusion The tasks, are authentic, encourage the students to reflect on the spiritual dimension of palliative care and are suitable for integration in the undergraduate medical curriculum.",
        document_order=14,
        coordinates="1,166.78,682.26,176.47,8.06;1,166.78,694.86,176.02,8.06;1,166.78,707.46,173.48,8.06;1,166.78,720.05,150.18,8.06",
    ),
    Text(
        content="What was already known?",
        document_order=16,
        coordinates="1,366.28,256.11,104.45,9.01",
    ),
    Text(
        content="► Insufficient education on four dimensions of palliative care in undergraduate medical curriculum.",
        document_order=17,
        coordinates="1,366.27,267.11,160.84,9.23;1,378.28,278.11,154.38,9.01;1,378.28,289.11,40.11,9.01",
    ),
    Text(
        content="► Especially the spiritual dimension is hardly addressed.",
        document_order=18,
        coordinates="1,366.27,300.11,164.09,9.23;1,378.28,311.11,38.66,9.01",
    ),
    Text(
        content="► A coherent set of learning tasks developed in line with instructional design guidelines.",
        document_order=20,
        coordinates="1,366.27,339.11,165.32,9.23;1,378.28,350.11,153.86,9.01",
    ),
    Text(
        content="► Stakeholder evaluations positive; confirm that these are authentic and encourage reflection.",
        document_order=21,
        coordinates="1,366.27,361.11,159.56,9.23;1,378.28,372.11,141.75,9.01;1,378.28,383.11,36.05,9.01",
    ),
    Text(
        content="What is their significance?",
        document_order=22,
        coordinates="1,366.28,400.11,104.57,9.01",
    ),
    Text(
        content="a. Clinical: Enhances palliative care education for medical students.",
        document_order=23,
        coordinates="1,366.28,411.11,166.50,9.01;1,378.28,422.11,75.08,9.01",
    ),
    Text(content="b.", document_order=24, coordinates="1,366.28,433.11,6.50,9.01"),
    Text(
        content="Research: Suitable for integration in undergraduate medical curriculum.",
        document_order=25,
        coordinates="1,378.28,433.11,128.72,9.01;1,378.28,444.11,125.74,9.01",
    ),
    Text(
        content="copyright.",
        document_order=26,
        coordinates="1,567.14,376.44,8.32,39.01",
    ),
    Text(
        content="The need for palliative care is set to grow due to demographic changes, longer disease trajectories and higher comorbidity.",
        document_order=28,
        coordinates="1,360.28,498.01,178.54,9.36;1,360.28,510.17,178.57,9.36;1,360.28,522.33,145.45,9.36",
    ),
    Text(
        content="Central to providing palliative care is the holistic, patient-centred and multidimensional approach, which addresses not only the physical, but also the psychological, social and spiritual dimension. 1",
        document_order=29,
        coordinates="1,507.95,522.33,30.90,9.36;1,360.28,534.49,178.57,9.36;1,360.28,546.65,178.56,9.36;1,360.28,558.81,178.60,9.36;1,360.28,570.97,178.57,9.36;1,360.28,583.13,104.24,9.36;1,464.27,580.99,3.69,6.21",
    ),
    Text(
        content="Providing palliative care is increasingly recognised as a universal responsibility of healthcare professionals 2 3 and all doctors will see patients with progressive life-limiting conditions at some point during their careers. 4",
        document_order=30,
        coordinates="1,473.03,583.13,65.74,9.36;1,360.27,595.29,178.56,9.36;1,360.27,607.45,178.58,9.36;1,360.27,619.61,27.60,9.36;1,387.67,617.47,10.12,6.21;1,401.99,619.61,136.83,9.36;1,360.28,631.77,178.53,9.36;1,360.28,643.93,146.67,9.36;1,506.67,641.79,3.69,6.21",
    ),
    Text(
        content="Physicians, irrespective of specialism, should be both competent and confident in caring for the palliative care patient.",
        document_order=31,
        coordinates="1,513.91,643.93,24.87,9.36;1,360.28,656.09,178.57,9.36;1,360.28,668.25,178.57,9.36;1,360.28,680.41,111.83,9.36",
    ),
    Text(
        content="Taking care of palliative care patients is typically associated with powerful and highly emotional situations affecting junior doctor's emotional well-being. 5",
        document_order=32,
        coordinates="1,476.55,680.41,62.29,9.36;1,360.28,692.57,178.57,9.36;1,360.28,704.73,178.50,9.36;1,360.28,716.89,178.58,9.36;1,360.28,729.05,45.08,9.36;1,405.15,726.91,3.69,6.21",
    ),
    Text(
        content="It is therefore important that Original research junior doctors develop the ability to guide palliative care patients during their medical training. 6",
        document_order=33,
        coordinates="1,413.24,729.05,125.59,9.36;2,60.50,24.52,85.87,9.48;2,56.50,45.11,232.01,9.36;2,56.50,57.11,155.00,9.36;2,211.23,54.96,3.69,6.21",
    ),
    Text(
        content="lthough there is a growing international movement to embed palliative care education in the undergraduate medical curricula, 5 this topic is not adequately addressed within all European medical universities.",
        document_order=34,
        coordinates="2,65.50,69.11,222.87,9.36;2,56.50,81.11,231.89,9.36;2,56.50,93.11,101.07,9.36;2,157.56,90.96,3.69,6.21;2,165.88,93.11,122.50,9.36;2,56.50,105.11,231.88,9.36",
    ),
    Text(
        content="Several studies demonstrate that medical students do not receive sufficient education in this area. 7 8",
        document_order=35,
        coordinates="2,56.50,117.11,231.88,9.36;2,56.50,129.11,184.10,9.36;2,240.59,126.96,8.94,6.21",
    ),
    Text(
        content="Students do not feel well prepared [9] [10] [11] [12] and feel especially ill-prepared to raise and discuss the psychological, social and spiritual dimensions of care. 13",
        document_order=36,
        coordinates="2,251.89,129.11,36.49,9.36;2,56.50,141.11,117.08,9.36;2,173.58,138.96,14.37,6.21;2,192.97,141.11,95.43,9.36;2,56.50,153.11,231.90,9.36;2,56.50,165.11,148.73,9.36;2,205.23,162.96,7.37,6.21",
    ),
    Text(
        content="Their education primarily focuses on one dimension-the physicalwhile allowing the others to fall by the wayside. 14",
        document_order=37,
        coordinates="2,217.75,165.11,70.64,9.36;2,56.50,177.11,231.90,9.36;2,56.50,189.11,224.52,9.36;2,281.01,186.96,7.37,6.21",
    ),
    Text(
        content="tudents also report that self-care and reflection in the context of palliative care do not get much attention in their education. 9 13",
        document_order=38,
        coordinates="2,56.50,201.11,231.90,9.36;2,56.50,213.11,231.90,9.36;2,56.50,225.11,67.49,9.36;2,123.99,222.96,12.78,6.21",
    ),
    Text(
        content="In the Netherlands, the undergraduate medical education assigns only limited attention on palliative and end-of-life care. 13 15-17",
        document_order=39,
        coordinates="2,139.37,225.11,149.01,9.36;2,56.50,237.11,231.88,9.36;2,56.50,249.11,146.92,9.36;2,203.41,246.96,28.09,6.21",
    ),
    Text(
        content="This despite that the national competency framework states that the doctor should promote people's health and related quality of life, also in the palliative phase. 18",
        document_order=40,
        coordinates="2,235.51,249.11,52.87,9.36;2,56.50,261.11,231.88,9.36;2,56.50,273.11,231.90,9.36;2,56.50,285.11,172.10,9.36;2,228.59,282.96,7.37,6.21",
    ),
    Text(
        content="The competences that Dutch medical students need to acquire to provide good-quality palliative care have recently been set out in an educational framework. 19",
        document_order=41,
        coordinates="2,237.86,285.11,50.53,9.36;2,56.50,297.11,231.89,9.36;2,56.50,309.11,231.89,9.36;2,56.50,321.11,168.01,9.36;2,224.50,318.96,7.37,6.21",
    ),
    Text(
        content="This framework specifies among others that the medical students should be able to talk to the patient and family about the incurable illness, prognosis and death, and discuss the four dimensions of care.",
        document_order=42,
        coordinates="2,236.71,321.11,51.68,9.36;2,56.50,333.11,231.88,9.36;2,56.50,345.11,231.90,9.36;2,56.50,357.11,231.89,9.36;2,56.50,369.11,121.76,9.36",
    ),
    Text(
        content="They should also be able to take care of their own well-being and reflect on their own spiritual needs, alongside their perceptions about life, death and dying.",
        document_order=43,
        coordinates="2,181.41,369.11,106.99,9.36;2,56.50,381.11,231.88,9.36;2,56.50,393.11,231.89,9.36;2,56.50,405.11,117.74,9.36",
    ),
    Text(
        content="To bridge the gap between what students should learn and actually learn about spiritual care, we developed a coherent set of eight learning tasks.",
        document_order=44,
        coordinates="2,65.50,417.11,222.89,9.36;2,56.50,429.11,231.91,9.36;2,56.50,441.11,182.38,9.36",
    ),
    Text(
        content="Addressing the spiritual dimension is a complex task.",
        document_order=45,
        coordinates="2,241.57,441.11,46.81,9.36;2,56.50,453.11,184.25,9.36",
    ),
    Text(
        content="According to current educational principles, learning complex tasks can be supported by providing authentic or realistic learning tasks 20, by using principles of reflective learning, and should be integrated in the curricula.",
        document_order=46,
        coordinates="2,244.73,453.11,43.66,9.36;2,56.50,465.11,231.90,9.36;2,56.50,477.11,231.90,9.36;2,56.50,489.11,80.12,9.36;2,136.62,486.96,7.37,6.21;2,144.00,489.11,144.40,9.36;2,56.50,501.11,231.89,9.36",
    ),
    Text(
        content="Authentic tasks allow students to acquire knowledge, skills and attitudes in an integrated fashion, 21 which improves the transfer of the curriculum to the workplace. 20",
        document_order=47,
        coordinates="2,56.50,513.11,231.89,9.36;2,56.50,525.11,194.45,9.36;2,250.94,522.96,7.37,6.21;2,262.50,525.11,25.89,9.36;2,56.50,537.11,231.90,9.36;2,56.50,549.11,24.87,9.36;2,81.36,546.96,7.37,6.21",
    ),
    Text(
        content="These authentic learning tasks can be interwoven in existing curricula in a horizontal and vertical integration manner.",
        document_order=48,
        coordinates="2,93.25,549.11,195.14,9.36;2,56.50,561.11,231.90,9.36;2,56.50,573.11,84.74,9.36",
    ),
    Text(
        content="3] [24] [25] Through reflection, students are encouraged to think about their role as a physician, 22 foster professional growth, release the emotional burden of caring for palliative care patients and increase patient care skills. 24",
        document_order=49,
        coordinates="2,91.86,594.96,7.22,6.21;2,101.14,597.11,187.26,9.36;2,56.50,609.11,165.28,9.36;2,221.77,606.96,7.37,6.21;2,231.56,609.11,56.83,9.36;2,56.50,621.11,231.89,9.36;2,56.50,633.11,231.89,9.36;2,56.50,645.11,23.83,9.36;2,80.32,642.96,7.37,6.21",
    ),
    Text(
        content="Self-reflective training on the spiritual dimensions within the students' own lives is recommended. 2",
        document_order=50,
        coordinates="2,90.92,645.11,197.48,9.36;2,56.51,657.11,227.44,9.36;2,283.94,654.96,3.69,6.21",
    ),
    Text(
        content="e developed a coherent set of realistic authentic learning tasks, in which students learn about and reflect on communication about the four dimensions of care, with a particular focus on the spiritual dimension.",
        document_order=51,
        coordinates="2,65.50,669.11,222.90,9.36;2,56.50,681.11,231.90,9.36;2,56.50,693.11,231.88,9.36;2,56.50,705.11,212.47,9.36",
    ),
    Text(
        content="The main aims of these learning tasks are that students learn about spiritual care, are able to talk about it with a palliative care patient, and to reflect on their spiritual experiences regarding life and death.",
        document_order=52,
        coordinates="2,271.54,705.11,16.86,9.36;2,56.50,717.11,231.88,9.36;2,56.50,729.11,231.90,9.36;2,306.89,45.11,231.90,9.36;2,306.89,57.11,157.54,9.36",
    ),
    Text(
        content="This article gives more insight into the usability and feasibility of these learning tasks from the stakeholders' perspectives, that is, medical students, teachers and educational scientists on the design of the learning tasks based on the educational principles of authentic educational scenarios, reflection and integration.",
        document_order=53,
        coordinates="2,467.16,57.11,71.62,9.36;2,306.89,69.11,231.90,9.36;2,306.89,81.11,231.88,9.36;2,306.89,93.11,231.89,9.36;2,306.89,105.11,231.89,9.36;2,306.89,117.11,231.90,9.36;2,306.89,129.11,115.41,9.36",
    ),
    Text(
        content="The research question is: How do medical students, teachers and educational scientists evaluate a set of coherent learning tasks focusing on the spiritual dimension of palliative care?",
        document_order=54,
        coordinates="2,426.79,129.11,112.00,9.36;2,306.89,141.11,231.89,9.36;2,306.89,153.11,231.90,9.36;2,306.89,165.11,228.96,9.36",
    ),
    Text(
        content="Three groups of stakeholders were asked to participate in this evaluation: medical students, teachers, and educational scientists.",
        document_order=57,
        coordinates="2,306.89,211.61,231.88,9.36;2,306.89,223.61,231.90,9.36;2,306.89,235.61,93.84,9.36",
    ),
    Text(
        content="The students were interviewed in focus groups.",
        document_order=58,
        coordinates="2,404.50,235.61,134.28,9.36;2,306.89,247.61,70.68,9.36",
    ),
    Text(
        content="The teachers and educational scientists were questioned in individual interviews, due to their busy schedules.",
        document_order=59,
        coordinates="2,381.54,247.61,157.23,9.36;2,306.89,259.61,231.89,9.36;2,306.89,271.61,92.69,9.36",
    ),
    Text(
        content="This qualitative approach was used to gather in-depth information and insights from our stakeholders.",
        document_order=60,
        coordinates="2,404.55,271.61,134.24,9.36;2,306.89,283.61,231.88,9.36;2,306.89,295.61,73.76,9.36",
    ),
    Text(
        content="In the Netherlands, it takes 6 years to qualify as a physician.",
        document_order=62,
        coordinates="2,306.89,330.11,231.88,9.36;2,306.89,342.11,20.24,9.36",
    ),
    Text(
        content="In the first 3 years, the Bachelor's program, the student primarily acquires theory and medical knowledge.",
        document_order=63,
        coordinates="2,330.85,342.11,207.93,9.36;2,306.89,354.11,231.89,9.36;2,306.89,366.11,22.54,9.36",
    ),
    Text(
        content="In the last 3 years, the Master's program, the focus is on the application of knowledge in the work setting by letting students rotate between different internships.",
        document_order=64,
        coordinates="2,334.14,366.11,204.63,9.36;2,306.89,378.11,231.90,9.36;2,306.89,390.11,231.88,9.36;2,306.89,402.11,49.79,9.36",
    ),
    Text(
        content="We designed a set of eight learning tasks (table 1; for a full description, see online supplemental appendix 1), designed to be integrated into the undergraduate medical curriculum.",
        document_order=66,
        coordinates="2,306.89,436.61,231.86,9.36;2,306.89,448.61,231.89,9.36;2,306.89,460.61,231.87,9.36;2,306.89,472.61,86.70,9.36",
    ),
    Text(
        content="The designers included diversity and variations in teaching methods, diseases, treatment plans, age and gender of the patient.",
        document_order=67,
        coordinates="2,397.51,472.61,141.26,9.36;2,306.89,484.61,231.89,9.36;2,306.89,496.61,178.30,9.36",
    ),
    Text(
        content="The competencies to be acquired are described in box 1.",
        document_order=68,
        coordinates="2,487.66,496.61,51.11,9.36;2,306.89,508.61,202.74,9.36",
    ),
    Text(
        content="These competences are a selection of the framework from Pieters et al. 19 The educational principles of authenticity, and reflection are incorporated into the set of learning tasks (see table 2).",
        document_order=69,
        coordinates="2,513.58,508.61,25.19,9.36;2,306.89,520.61,231.89,9.36;2,306.89,532.61,52.49,9.36;2,359.38,530.46,7.37,6.21;2,315.89,544.61,222.90,9.36;2,306.89,556.61,231.90,9.36;2,306.89,568.61,77.61,9.36",
    ),
    Text(
        content="Three groups of stakeholders were asked to participate in the evaluation: medical students, teachers and educational scientists.",
        document_order=72,
        coordinates="3,56.50,236.21,231.88,9.36;3,56.50,248.21,231.90,9.36;3,56.50,260.21,95.79,9.36",
    ),
    Text(
        content="The stakeholders came from faculties of medicine of four different universities in the Netherlands.",
        document_order=73,
        coordinates="3,158.01,260.21,130.37,9.36;3,56.50,272.21,231.88,9.36;3,56.50,284.21,71.47,9.36",
    ),
    Text(
        content="These stakeholders were asked to be interviewed in focus groups as they represented the educational users as learners.",
        document_order=75,
        coordinates="3,56.50,320.05,231.89,9.36;3,56.50,332.05,231.87,9.36;3,56.50,344.05,48.14,9.36",
    ),
    Text(
        content="Medical students in their final year of the Bachelor's program or studying for their Master's degree were invited.",
        document_order=76,
        coordinates="3,107.86,344.05,180.53,9.36;3,56.50,356.05,231.88,9.36;3,56.50,368.05,87.16,9.36",
    ),
    Text(
        content="These students have an informed opinion as to which tasks they deemed suitable for students and at what stage the tasks could best be implemented in the curriculum.",
        document_order=77,
        coordinates="3,146.62,368.05,141.78,9.36;3,56.50,380.05,231.87,9.36;3,56.50,392.05,231.90,9.36;3,56.50,404.05,135.74,9.36",
    ),
    Text(
        content="These stakeholders were invited for their insight and experience in education and their substantive expertise in palliative care.",
        document_order=79,
        coordinates="3,56.50,439.89,231.87,9.36;3,56.50,451.89,231.88,9.36;3,56.50,463.89,73.68,9.36",
    ),
    Text(
        content="This group of stakeholders included medical specialists, mental healthcare providers and psychologists involved in teaching in undergraduate medical education.",
        document_order=80,
        coordinates="3,133.20,463.89,155.20,9.36;3,56.50,475.89,231.88,9.36;3,56.50,487.89,231.89,9.36;3,56.50,499.89,80.65,9.36",
    ),
    Text(
        content="Educational scientists (N=4)",
        document_order=81,
        coordinates="3,306.89,44.93,87.73,7.82",
    ),
    Text(
        content="These stakeholders were asked for their expertise in both educational design and the educational principles used in this learning program (Authentic learning, reflection and integration into existing courses).",
        document_order=82,
        coordinates="3,306.89,55.70,231.90,9.36;3,306.89,67.70,231.90,9.36;3,306.89,79.70,231.89,9.36;3,306.89,91.70,211.09,9.36",
    ),
    Text(
        content="The educational scientists worked at medical faculties.",
        document_order=83,
        coordinates="3,521.90,91.70,16.86,9.36;3,306.89,103.70,212.67,9.36",
    ),
    Text(
        content="The teachers and educational scientists were interviewed individually, the students were interviewed in focus groups, using the same semistructured interview guide (see online supplemental appendix 2).",
        document_order=85,
        coordinates="3,306.89,140.01,231.89,9.36;3,306.89,152.01,231.88,9.36;3,306.89,164.01,231.90,9.36;3,306.89,176.01,187.04,9.36",
    ),
    Text(
        content="The interview guide asked for perceptions of the set of learning tasks, focusing on the educational learning principles that shaped them: authentic learning tasks, the principles of reflective learning, and the integration into the existing courses.",
        document_order=86,
        coordinates="3,496.36,176.01,42.42,9.36;3,306.89,188.01,231.89,9.36;3,306.89,200.01,231.89,9.36;3,306.89,212.01,231.88,9.36;3,306.89,224.01,231.88,9.36;3,306.89,236.01,70.09,9.36",
    ),
    Text(
        content="Participants were recruited through purposeful sampling within the network of Pasemeco until data saturation was reached.",
        document_order=88,
        coordinates="3,306.89,272.32,231.89,9.36;3,306.89,284.32,231.91,9.36;3,306.89,296.32,105.21,9.36",
    ),
    Text(
        content="They were invited through an email that included the information letter.",
        document_order=89,
        coordinates="3,417.20,296.32,121.57,9.36;3,306.89,308.32,195.27,9.36",
    ),
    Text(
        content="Prior to their individual or focus group interview, the participants received a short explanatory video and a document with an overview of the set of learning tasks.",
        document_order=90,
        coordinates="3,505.29,308.32,33.50,9.36;3,306.89,320.32,231.90,9.36;3,306.89,332.32,231.89,9.36;3,306.89,344.32,231.88,9.36",
    ),
    Text(
        content="The interviews took no more than 45 min and were conducted by JP and EN.",
        document_order=91,
        coordinates="3,306.89,356.32,231.90,9.36;3,306.89,368.32,109.85,9.36",
    ),
    Text(
        content="The interviewees gave their written informed consent.",
        document_order=92,
        coordinates="3,419.96,368.32,118.81,9.36;3,306.89,380.32,111.65,9.36",
    ),
    Text(
        content="The interviews were recorded and transcribed.",
        document_order=94,
        coordinates="3,306.89,416.64,215.11,9.36",
    ),
    Text(
        content="To support the qualitative data analysis, Atlas.",
        document_order=95,
        coordinates="3,527.88,416.64,10.90,9.36;3,306.89,428.64,188.59,9.36",
    ),
    Text(
        content="ti V.8 was used.",
        document_order=96,
        coordinates="3,495.48,428.64,43.29,9.36;3,306.89,440.64,22.13,9.36",
    ),
    Text(
        content="The transcripts were analysed using template analysis, taking into account the step-by-step plan of Brooks et al. 26 Researchers JP, EN, and FW carried out the preliminary coding of the data, starting with determining the a priori themes.",
        document_order=97,
        coordinates="3,334.24,440.64,204.54,9.36;3,306.89,452.64,231.88,9.36;3,306.88,464.64,57.78,9.36;3,364.67,462.49,7.37,6.21;3,376.65,464.64,162.13,9.36;3,306.89,476.64,231.90,9.36;3,306.89,488.64,143.68,9.36",
    ),
    Text(
        content="These themes were based on the components of the research question (authentic learning tasks; reflection and integration into the curriculum).",
        document_order=98,
        coordinates="3,454.64,488.64,84.12,9.36;3,306.89,500.64,231.89,9.36;3,306.89,512.64,231.89,9.36;3,306.89,524.64,91.86,9.36",
    ),
    Text(
        content="Two interview transcripts were read and coded independently by researchers JP, EN, and FW.",
        document_order=99,
        coordinates="3,402.84,524.64,135.94,9.36;3,306.89,536.64,231.88,9.36;3,306.89,548.64,37.37,9.36",
    ),
    Text(
        content="They discussed their findings, merged the themes into meaningful clusters, and provided an initial coding template.",
        document_order=100,
        coordinates="3,349.37,548.64,189.39,9.36;3,306.89,560.64,231.90,9.36;3,306.89,572.64,98.00,9.36",
    ),
    Text(
        content="This template was then applied independently by the three researchers to three other transcripts.",
        document_order=101,
        coordinates="3,407.19,572.64,131.59,9.36;3,306.89,584.64,231.89,9.36;3,306.89,596.64,47.56,9.36",
    ),
    Text(
        content="After consultation, the template was finalised and applied to the full data set.",
        document_order=102,
        coordinates="3,315.89,608.64,222.88,9.36;3,306.89,620.64,124.20,9.36",
    ),
    Text(
        content="Themes were discussed and elaborated on iteratively with the whole research team.",
        document_order=103,
        coordinates="3,435.75,620.64,103.02,9.36;3,306.89,632.64,231.90,9.36;3,306.89,644.64,23.64,9.36",
    ),
    Text(
        content="JP and DV coded the other eight transcripts independently and discussed the results afterward.",
        document_order=104,
        coordinates="3,335.58,644.64,203.19,9.36;3,306.89,656.64,212.79,9.36",
    ),
    Text(
        content="The results were then discussed among all of the authors.",
        document_order=105,
        coordinates="3,521.92,656.64,16.86,9.36;3,306.89,668.64,225.50,9.36",
    ),
    Text(
        content="This learning program was developed by a multidisciplinary group that included educational scientists (DV and DD), researchers (JP and EN) and physicians",
        document_order=107,
        coordinates="3,306.89,704.95,231.89,9.36;3,306.89,716.95,231.89,9.36;3,306.89,728.95,231.90,9.36",
    ),
    Text(
        content="Competencies:",
        document_order=109,
        coordinates="3,62.50,84.59,58.25,9.01",
    ),
    Text(
        content="1) The student communicates in a respectful and empathetic manner with patients and relatives.",
        document_order=110,
        coordinates="3,62.50,95.59,216.64,9.01;3,62.50,106.59,127.30,9.01",
    ),
    Text(
        content="2) The student makes the four dimensions (somatic, psychological, social and spiritual) of palliative care discussable with the patient and family.",
        document_order=111,
        coordinates="3,62.50,117.60,184.98,9.01;3,62.50,128.60,184.29,9.01;3,62.50,139.60,143.12,9.01",
    ),
    Text(
        content="3) The student reflects on distance and closeness in the treatment relationship with a palliative patient.",
        document_order=112,
        coordinates="3,62.50,150.60,197.81,9.01;3,62.50,161.60,170.37,9.01",
    ),
    Text(
        content="4) The student reflects on his/her spiritual and existential views around life and death.",
        document_order=113,
        coordinates="3,62.50,172.60,203.60,9.01;3,62.50,183.60,102.51,9.01",
    ),
    Text(
        content="The stakeholders agreed that the educational materials, including the case descriptions, the video clips and short movies, showed the students a realistic view of what they could encounter in the workplace.",
        document_order=116,
        coordinates="4,56.50,129.06,231.90,9.36;4,56.50,141.06,231.90,9.36;4,56.50,153.06,231.88,9.36;4,56.50,165.06,231.90,9.36",
    ),
    Text(
        content="The learning tasks were authentic and presented in a logical and structured order, from paper cases to a fullfledged conversation with a patient.",
        document_order=117,
        coordinates="4,56.50,177.06,231.89,9.36;4,56.50,189.06,231.90,9.36;4,56.50,201.06,155.31,9.36",
    ),
    Text(
        content="The stakeholders commented that the learning tasks and materials could be further improved if they provided a better reflection of the cultural diversity within the patient population.",
        document_order=118,
        coordinates="4,215.03,201.06,73.37,9.36;4,56.50,213.06,231.90,9.36;4,56.50,225.06,231.89,9.36;4,56.50,237.06,231.90,9.36",
    ),
    Text(
        content="Students especially appreciated the clips in which real patients and doctors talked about palliative care and suggested that encouraging the possibility to discuss cases students have encountered in medical practice would further increase the authenticity.",
        document_order=119,
        coordinates="4,56.50,249.06,231.90,9.36;4,56.50,261.06,231.89,9.36;4,56.50,273.06,231.89,9.36;4,56.50,285.06,231.90,9.36;4,56.50,297.06,168.17,9.36",
    ),
    Text(
        content="Stakeholders recognised reflection is a recurring element across the learning tasks.",
        document_order=121,
        coordinates="4,56.50,333.01,231.88,9.36;4,56.50,345.01,141.35,9.36",
    ),
    Text(
        content="They also consider it to be an important skill.",
        document_order=122,
        coordinates="4,200.31,345.01,88.06,9.36;4,56.50,357.01,100.91,9.36",
    ),
    Text(
        content="According to the stakeholders, the majority of the students should be able to reflect well on the various health dimensions, but the spiritual dimension can be emotionally charged.",
        document_order=123,
        coordinates="4,159.63,357.01,128.75,9.36;4,56.50,369.01,231.90,9.36;4,56.50,381.01,231.90,9.36;4,56.50,393.01,174.42,9.36",
    ),
    Text(
        content="Some stakeholders indicated that to be able to reflect on this properly, some life experiences would not go amiss.",
        document_order=124,
        coordinates="4,235.46,393.01,52.94,9.36;4,56.50,405.01,231.89,9.36;4,56.50,417.01,198.88,9.36",
    ),
    Text(
        content="Novice medical students' reflections lack the necessary depth in comparison with Master's degree students.",
        document_order=125,
        coordinates="4,257.91,417.01,30.47,9.36;4,56.50,429.01,231.88,9.36;4,56.50,441.01,192.96,9.36",
    ),
    Text(
        content="Both the teachers and students preferred oral group reflection.",
        document_order=126,
        coordinates="4,251.93,441.01,36.47,9.36;4,56.50,453.01,231.88,9.36",
    ),
    Text(
        content="The students indicated that they attached great value to the interaction with their fellow students and that it helps them express themselves better.",
        document_order=127,
        coordinates="4,56.50,465.01,231.90,9.36;4,56.50,477.01,231.89,9.36;4,56.50,489.01,168.94,9.36",
    ),
    Text(
        content="Student safety must be ensured in order for them to properly reflect in a group.",
        document_order=128,
        coordinates="4,228.24,489.01,60.14,9.36;4,56.50,501.01,231.88,9.36;4,56.50,513.01,46.77,9.36",
    ),
    Text(
        content="The stakeholders believed that the learning tasks should be integrated across the curriculum in different years.",
        document_order=130,
        coordinates="4,56.50,548.96,231.88,9.36;4,56.50,560.96,231.88,9.36",
    ),
    Text(
        content="However, it is important that this does not become too fragmented and that students can clearly see the cohesion.",
        document_order=131,
        coordinates="4,56.50,572.96,231.89,9.36;4,56.50,584.96,231.89,9.36;4,56.50,596.96,20.38,9.36",
    ),
    Text(
        content="Almost all stakeholders mentioned that the initial tasks (tasks 1-5) would be best implemented in the Bachelor's program, as the cases in these tasks revolve around the basis of palliative care.",
        document_order=132,
        coordinates="4,79.30,596.96,209.08,9.36;4,56.50,608.96,231.91,9.36;4,56.50,620.96,231.89,9.36;4,56.50,632.96,148.00,9.36",
    ),
    Text(
        content="The other learning tasks (tasks 6-8) were considered more appropriate for more advanced students during the internships as these center around communication with a simulated or real patient.",
        document_order=133,
        coordinates="4,207.59,632.96,80.81,9.36;4,56.50,644.96,231.89,9.36;4,56.50,656.96,231.89,9.36;4,56.50,668.96,231.88,9.36;4,56.50,680.96,92.17,9.36",
    ),
    Text(
        content="According to the stakeholders, they required experience with patients that students only acquire during the Master's degree.",
        document_order=134,
        coordinates="4,153.08,680.96,135.29,9.36;4,56.50,692.96,231.88,9.36;4,56.50,704.96,181.77,9.36",
    ),
    Text(
        content="There was no consensus as to when to start the learning trajectory.",
        document_order=135,
        coordinates="4,242.68,704.96,45.72,9.36;4,56.50,716.96,231.90,9.36;4,56.50,728.96,19.29,9.36",
    ),
    Text(
        content="Some stakeholders believed that palliative care education should start in the very first year, so that students become immediately aware that palliative care is a part of routine care.",
        document_order=136,
        coordinates="4,80.35,728.96,208.04,9.36;4,306.89,45.11,231.89,9.36;4,306.89,57.11,231.90,9.36;4,306.89,69.11,133.09,9.36",
    ),
    Text(
        content="But others thought it better to wait until the end of the Bachelor's program, because students would not be open to the subject or not fully understand the subject matter until then.",
        document_order=137,
        coordinates="4,444.37,69.11,94.41,9.36;4,306.89,81.11,231.89,9.36;4,306.89,93.11,231.89,9.36;4,306.89,105.11,213.52,9.36",
    ),
    Text(
        content="The implementation should also take into account the differences between students.",
        document_order=138,
        coordinates="4,315.89,117.11,222.89,9.36;4,306.89,129.11,142.94,9.36",
    ),
    Text(
        content="In the final learning task, students conduct an unsupervised interview with a palliative patient.",
        document_order=139,
        coordinates="4,452.97,129.11,85.81,9.36;4,306.89,141.11,231.89,9.36;4,306.89,153.11,81.89,9.36",
    ),
    Text(
        content="According to the stakeholders, the learning program does prepare students well for this interview, but it is still an emotionally charged task.",
        document_order=140,
        coordinates="4,391.67,153.11,147.11,9.36;4,306.89,165.11,231.88,9.36;4,306.89,177.11,231.90,9.36",
    ),
    Text(
        content="In order to protect both the patients and the students, the students must be well prepared and be able to take the lead in such an interview.",
        document_order=141,
        coordinates="4,306.89,189.11,231.89,9.36;4,306.89,201.11,231.90,9.36;4,306.89,213.11,124.16,9.36",
    ),
    Text(
        content="Some students may need more training or support (table 3).",
        document_order=142,
        coordinates="4,433.77,213.11,105.03,9.36;4,306.89,225.11,147.84,9.36",
    ),
    Text(
        content="The medical students, teachers, and educational scientists agree that the set of learning tasks was designed in line with contemporary instructional design guidelines.",
        document_order=144,
        coordinates="4,306.89,261.11,231.89,9.36;4,306.89,273.11,231.90,9.36;4,306.89,285.11,231.89,9.36;4,306.89,297.11,22.23,9.36",
    ),
    Text(
        content="Learning was clearly organised around authentic learning tasks relevant to the later profession, using paper, video cases, as well as simulations and real patients.",
        document_order=145,
        coordinates="4,331.78,297.11,207.01,9.36;4,306.89,309.11,231.89,9.36;4,306.89,321.11,231.89,9.36;4,306.89,333.11,36.27,9.36",
    ),
    Text(
        content="The tasks encourage the students to reflect on the four dimensions of palliative care and their personal values.",
        document_order=146,
        coordinates="4,347.41,333.11,191.36,9.36;4,306.89,345.11,231.88,9.36;4,306.89,357.11,69.73,9.36",
    ),
    Text(
        content="There were various options offered for the integration of the tasks into existing curricula.",
        document_order=147,
        coordinates="4,381.04,357.11,157.74,9.36;4,306.89,369.11,231.87,9.36",
    ),
    Text(
        content="The stakeholders also offered a number of suggestions to take into account, which will be discussed further.",
        document_order=148,
        coordinates="4,306.89,381.11,231.90,9.36;4,306.89,393.11,225.88,9.36",
    ),
    Text(
        content="First, palliative care and the spiritual dimension in particular are emotionally charged subjects.",
        document_order=149,
        coordinates="4,315.89,405.11,222.88,9.36;4,306.89,417.11,204.25,9.36",
    ),
    Text(
        content="Extra attention to both student and patient safety is required.",
        document_order=150,
        coordinates="4,515.34,417.11,23.44,9.36;4,306.89,429.11,231.88,9.36",
    ),
    Text(
        content="Both the students and teachers attached great value to the group discussions and reflections, where a bond of trust and psychological safety between all of the attendees was considered to be essential.",
        document_order=151,
        coordinates="4,306.89,441.11,231.88,9.36;4,306.89,453.11,231.87,9.36;4,306.89,465.11,231.87,9.36;4,306.89,477.11,178.53,9.36",
    ),
    Text(
        content="These findings are in line with the literature, where confidentially sharing experiences is needed and only possible in a group of people who know each other. 2 27 Second, the educational materials were considered authentic with variation in cases and learning methods, but to increase authenticity, the stakeholders suggested including more cultural diversity among the patient cases used in the learning tasks.",
        document_order=152,
        coordinates="4,489.22,477.11,49.57,9.36;4,306.89,489.11,231.90,9.36;4,306.89,501.11,231.90,9.36;4,306.89,513.11,166.83,9.36;4,473.72,510.96,12.90,6.21;4,315.89,525.11,222.88,9.36;4,306.89,537.11,231.89,9.36;4,306.89,549.11,231.89,9.36;4,306.89,561.11,231.89,9.36;4,306.89,573.11,134.15,9.36",
    ),
    Text(
        content="Contemporary society is more culturally diverse than the current materials reflected.",
        document_order=153,
        coordinates="4,443.75,573.11,95.04,9.36;4,306.89,585.11,231.90,9.36;4,306.89,597.11,39.97,9.36",
    ),
    Text(
        content="It is an important topic that should not be overlooked, given that many physicians are unfamiliar with the specific needs of ethnic minorities regarding palliative care and communication. 28",
        document_order=154,
        coordinates="4,350.66,597.11,188.12,9.36;4,306.89,609.11,231.90,9.36;4,306.89,621.11,231.88,9.36;4,306.89,633.11,150.06,9.36;4,456.93,630.96,7.37,6.21",
    ),
    Text(
        content="hird, there was discussion on how to integrate learning tasks or palliative care education in general.",
        document_order=155,
        coordinates="4,315.89,645.11,222.89,9.36;4,306.89,657.11,231.89,9.36",
    ),
    Text(
        content="All participants agreed that this should start in the Bachelors and most agreed that it should be integrated vertically, throughout the undergraduate program and not as a stand-alone module.",
        document_order=156,
        coordinates="4,306.89,669.11,231.89,9.36;4,306.89,681.11,231.90,9.36;4,306.89,693.11,231.87,9.36;4,306.89,705.11,156.93,9.36",
    ),
    Text(
        content="Furthermore, it needs to be integrated horizontally, where relevant, for instance, in cardiology, oncology, humanities, and copyright.",
        document_order=157,
        coordinates="4,469.68,705.11,69.11,9.36;4,306.89,717.11,231.90,9.36;4,306.89,729.11,231.89,9.36;4,567.14,376.44,8.32,39.01",
    ),
    Text(
        content="on January 21, 2022 by guest.",
        document_order=158,
        coordinates="4,576.14,582.02,8.33,10.01;4,576.14,594.53,8.33,32.01;4,576.14,629.05,8.32,12.51;4,576.14,644.06,8.33,20.02;4,576.14,666.58,8.33,9.50;4,576.14,678.58,8.33,24.52",
    ),
    Text(
        content="Protected by http://spcare.bmj.com/",
        document_order=159,
        coordinates="4,576.14,705.60,8.33,38.52;4,576.14,746.62,8.33,9.50;4,576.14,490.99,8.33,88.53",
    ),
    Text(
        content="Original research communication training.",
        document_order=160,
        coordinates="5,448.91,24.52,85.87,9.48;5,56.50,512.98,104.79,9.36",
    ),
    Text(
        content="Integrating this set of learning tasks, therefore, mainly depends on the curriculum of a medical university and its identity as to where and when palliative care education can be implemented in the curriculum.",
        document_order=161,
        coordinates="5,163.19,512.98,125.21,9.36;5,56.50,524.98,231.88,9.36;5,56.50,536.98,231.90,9.36;5,56.50,548.98,231.90,9.36;5,56.50,560.98,65.80,9.36",
    ),
    Text(
        content="The idea of vertically and horizontally integration is in line with recent educational research and guidelines. 4 29 30",
        document_order=162,
        coordinates="5,124.97,560.98,163.40,9.36;5,56.50,572.98,231.89,9.36;5,56.50,584.98,64.18,9.36;5,120.67,582.83,22.12,6.21",
    ),
    Text(
        content="ome stakeholders argued that for learning about spiritual and palliative care in general, students should have some life experience and, therefore, it would be more suitable to start the program later in the bachelor.",
        document_order=163,
        coordinates="5,65.50,596.98,222.90,9.36;5,56.50,608.98,231.89,9.36;5,56.50,620.98,231.89,9.36;5,56.50,632.98,231.90,9.36",
    ),
    Text(
        content="Others argue that palliative care should be normalised for the students and should, therefore, start in the first year.",
        document_order=164,
        coordinates="5,56.50,644.98,231.89,9.36;5,56.50,656.98,231.89,9.36;5,56.50,668.98,20.34,9.36",
    ),
    Text(
        content="The concern that early exposure may be emotionally challenging for young students, is the main reason why curricula integrate palliative care education in general later in the program. 31 32",
        document_order=165,
        coordinates="5,79.00,668.98,209.39,9.36;5,56.50,680.98,231.89,9.36;5,56.50,692.98,231.89,9.36;5,56.50,704.98,128.64,9.36;5,185.13,702.83,17.54,6.21",
    ),
    Text(
        content="However, research shows that direct experience with palliative care for first-year students is associated with positive effects on the students' attitudes regarding caring for palliative care patients. 29 31 33 34",
        document_order=166,
        coordinates="5,206.90,704.98,81.49,9.36;5,56.50,716.98,231.89,9.36;5,56.50,728.98,231.87,9.36;5,306.89,512.98,231.91,9.36;5,306.89,524.98,56.36,9.36;5,363.24,522.83,34.36,6.21",
    ),
    Text(
        content="Junior doctors who were trained earlier in palliative care have enhanced competencies of psychosocial and spiritual aspects of palliative care, communication, and self-awareness. 34",
        document_order=167,
        coordinates="5,400.07,524.98,138.71,9.36;5,306.89,536.98,231.89,9.36;5,306.89,548.98,231.90,9.36;5,306.89,560.98,164.04,9.36;5,470.92,558.83,7.37,6.21",
    ),
    Text(
        content="Thus, early exposure helps to normalise death and dying and the complex emotions that students and physicians can encounter while treating palliative care patients. 31 33 34",
        document_order=168,
        coordinates="5,486.00,560.98,52.77,9.36;5,306.88,572.98,231.89,9.36;5,306.88,584.98,231.89,9.36;5,306.88,596.98,206.08,9.36;5,512.96,594.83,25.81,6.21",
    ),
    Text(
        content="nterestingly, in this study, students themselves had lively discussions on this topic too, but they mainly discussed more practical obstacles: when is there time for this in the curriculum?",
        document_order=169,
        coordinates="5,306.89,608.98,231.89,9.36;5,306.89,620.98,231.88,9.36;5,306.89,632.98,231.87,9.36;5,306.89,644.98,112.32,9.36",
    ),
    Text(
        content="This study had some limitations.",
        document_order=170,
        coordinates="5,315.89,656.98,141.26,9.36",
    ),
    Text(
        content="To begin with, we evaluated the set of learning tasks prior to its implementation.",
        document_order=171,
        coordinates="5,460.51,656.98,78.29,9.36;5,306.89,668.98,231.88,9.36;5,306.89,680.98,46.39,9.36",
    ),
    Text(
        content="This meant that we could not reflect on the implementation process itself, leaving this to be researched at a later stage.",
        document_order=172,
        coordinates="5,357.66,680.98,181.12,9.36;5,306.89,692.98,231.89,9.36;5,306.89,704.98,137.26,9.36",
    ),
    Text(
        content="We also focused on the stakeholders in the educational setting: medical students, teachers, and educational scientists.",
        document_order=173,
        coordinates="5,449.30,704.98,89.46,9.36;5,306.89,716.98,231.89,9.36;5,306.89,728.98,195.29,9.36",
    ),
    Text(
        content="Patients'I would also pay more attention to a more diversified background,(…).",
        document_order=174,
        coordinates="5,505.64,728.98,33.14,9.36;5,108.50,156.07,221.01,8.06",
    ),
    Text(
        content="The impression here is that it might be more about the classic white Dutch native than perhaps the Surinamese or Moroccan who gets into these problems and needs an essentially different approach'-I7",
        document_order=175,
        coordinates="5,330.77,156.07,189.69,8.06;5,108.50,165.57,422.62,8.06;5,108.50,175.07,12.26,8.06",
    ),
    Text(
        content="'(the clips, eds.)in the sense that the doctors who were talking, for example a [person] I have met in the clinic as well so that appeals more to the imagination.",
        document_order=176,
        coordinates="5,108.50,203.57,426.67,8.06;5,108.50,213.08,59.04,8.06",
    ),
    Text(
        content="That actually makes it even more authentic'-FG2",
        document_order=177,
        coordinates="5,168.80,213.08,153.12,8.06",
    ),
    Text(
        content="'That there are not only videos but also something like a link to a wishlist, and a Volkskrant [newspaper] article so I think that's already very authentic.",
        document_order=178,
        coordinates="5,108.50,241.58,429.85,8.06;5,108.50,251.08,30.85,8.06",
    ),
    Text(
        content="You might want to make it a little more authentic by having students contribute cases they encounter'-FG2 Reflective learning'I believe, indeed, that in real life that might be better than on paper, especially because you sometimes have to put something on paper and then you are not really sure or you feel differently or have not enough time and if you are really working in such a group, then ideas emerge or feelings that other people then evoke in you or you hear it and you think, oh that's right, I agree or I do not'-FG1'What is also important here is that in your educational groups, or in the subgroup where you would discuss this, you have a bond of trust as well as feel safe'-I11",
        document_order=179,
        coordinates="5,140.60,251.08,334.78,8.06;5,60.50,263.46,29.61,8.06;5,60.50,272.96,25.03,8.06;5,108.50,263.46,419.16,8.06;5,108.50,272.96,418.97,8.06;5,108.50,282.46,386.39,8.06;5,108.50,310.96,424.83,8.06;5,108.50,320.47,76.74,8.06",
    ),
    Text(
        content="And what might also be good timing,(…), is the second half of the third year of medicine.",
        document_order=181,
        coordinates="5,108.50,332.84,277.17,8.06",
    ),
    Text(
        content="Students are then very receptive to everything that is useful in their internships, so to speak, because then it is kind of a big thing that you will have to tackle soon and so you have to get started'-FG2",
        document_order=182,
        coordinates="5,387.39,332.84,141.06,8.06;5,108.50,342.35,429.36,8.06;5,108.50,351.85,44.36,8.06",
    ),
    Text(
        content="'I see no reason not to do it (integration as of year 1, eds.).",
        document_order=183,
        coordinates="5,108.50,380.35,181.60,8.06",
    ),
    Text(
        content="And another advantage is that students will get an idea of-oh, yes, so this is part of the job as well?",
        document_order=184,
        coordinates="5,291.36,380.35,238.27,8.06;5,108.50,389.85,71.45,8.06",
    ),
    Text(
        content="It soon makes it more normal, because students often enrol with a strong idea of: we are going to make everyone better… but accepting that you can't make someone better will become the reality… but it is not really part of the idea of beginning students so, in that sense, I think: maybe it's also good to create some kind of awareness here'-I12",
        document_order=185,
        coordinates="5,181.99,389.85,349.34,8.06;5,108.50,399.35,409.56,8.06;5,108.50,408.86,305.78,8.06",
    ),
    Text(
        content="'I believe you could use that simulation interview as a go/no-go for having an interview with a patient.",
        document_order=186,
        coordinates="5,108.50,437.36,316.08,8.06",
    ),
    Text(
        content="And, once again, they really are vulnerable patients, often in the final stage of life, who are often quite willing to contribute to the training, but who should also not be burdened disproportionately by oafs or students who are not interested or cut corners, and that such a patient is about to go home with a bad feeling after 45 minutes'-I8 FG, Focus Group; I, Interview.",
        document_order=187,
        coordinates="5,425.84,437.36,97.24,8.06;5,108.50,446.86,414.15,8.06;5,108.50,456.36,425.00,8.06;5,108.50,465.87,102.09,8.06;5,60.50,478.19,90.18,8.06",
    ),
    Text(
        content="were not involved in the evaluation, although they were involved in the overarching project within which the learning tasks were developed.",
        document_order=188,
        coordinates="6,56.50,45.11,231.87,9.36;6,56.50,57.12,231.87,9.36;6,56.50,69.13,150.15,9.36",
    ),
    Text(
        content="Last but not least, the educational principles within this learning program were tailored to the Dutch situation.",
        document_order=189,
        coordinates="6,210.12,69.13,78.29,9.36;6,56.50,81.14,231.87,9.36;6,56.50,93.15,159.03,9.36",
    ),
    Text(
        content="The educational principles and general setup of the design are internationally transferable, if tailored to the national situation.",
        document_order=190,
        coordinates="6,218.82,93.15,69.57,9.36;6,56.50,105.16,231.89,9.36;6,56.50,117.17,231.90,9.36;6,56.50,129.18,39.88,9.36",
    ),
    Text(
        content="Following the authenticity principle means that it is important to paint a realistic picture of the professional field.",
        document_order=191,
        coordinates="6,100.44,129.18,187.95,9.36;6,56.50,141.19,231.90,9.36;6,56.50,153.20,77.26,9.36",
    ),
    Text(
        content="If authenticity is to be guaranteed, learning tasks will have to be reviewed and adapted to be used in other countries.",
        document_order=192,
        coordinates="6,137.41,153.20,150.97,9.36;6,56.50,165.21,231.89,9.36;6,56.50,177.22,127.15,9.36",
    ),
    Text(
        content="This also regards to the principle of reflective learning.",
        document_order=193,
        coordinates="6,186.79,177.22,101.60,9.36;6,56.50,189.23,133.47,9.36",
    ),
    Text(
        content="The students involved in this study are already familiar with reflecting and sharing their opinion, since it plays a vital role in their curriculum.",
        document_order=194,
        coordinates="6,193.19,189.23,95.19,9.36;6,56.50,201.24,231.89,9.36;6,56.50,213.25,231.88,9.36;6,56.50,225.26,49.64,9.36",
    ),
    Text(
        content="On a national level there is a lively debate on end-of-life care, but not on the spiritual dimension.",
        document_order=195,
        coordinates="6,108.94,225.26,179.46,9.36;6,56.50,237.27,231.89,9.36",
    ),
    Text(
        content="Therefore, an emphasis was placed on the spiritual dimension.",
        document_order=196,
        coordinates="6,56.51,249.28,231.88,9.36;6,56.51,261.29,47.17,9.36",
    ),
    Text(
        content="This study has several practical implications.",
        document_order=197,
        coordinates="6,65.51,273.30,196.78,9.36",
    ),
    Text(
        content="First, it pays off to integrate the program horizontally and vertically into the curriculum.",
        document_order=198,
        coordinates="6,266.39,273.30,22.01,9.36;6,56.51,285.31,231.87,9.36;6,56.51,297.32,160.16,9.36",
    ),
    Text(
        content="It depends on the specific tasks and the curriculum itself how and where the integration can best take place.",
        document_order=199,
        coordinates="6,222.91,297.32,65.48,9.36;6,56.51,309.33,231.90,9.36;6,56.51,321.34,181.09,9.36",
    ),
    Text(
        content="Some tasks will fit in well with education regarding communication or where clinical conditions are discussed such as oncology or lung disease.",
        document_order=200,
        coordinates="6,240.93,321.34,47.47,9.36;6,56.51,333.35,231.90,9.36;6,56.51,345.36,231.87,9.36;6,56.51,357.37,109.08,9.36",
    ),
    Text(
        content="To avoid fragmentation and guarantee that all aspects are covered, however, it is also important that someone has an overview of where and how palliative care is addressed in the curriculum, for example, a curriculum coordinator or someone specifically assigned with this task.",
        document_order=201,
        coordinates="6,168.62,357.37,119.77,9.36;6,56.51,369.38,231.90,9.36;6,56.51,381.39,231.88,9.36;6,56.51,393.40,231.89,9.36;6,56.51,405.41,231.88,9.36;6,56.51,417.42,153.03,9.36",
    ),
    Text(
        content="Furthermore, the tasks can always be adapted to specific contexts.",
        document_order=202,
        coordinates="6,213.64,417.42,74.76,9.36;6,56.51,429.43,213.40,9.36",
    ),
    Text(
        content="For example, it might be difficult to arrange interviews with palliative care patients.",
        document_order=203,
        coordinates="6,273.72,429.43,14.69,9.36;6,56.51,441.44,231.89,9.36;6,56.51,453.45,119.44,9.36",
    ),
    Text(
        content="Students could then interview a chronically ill patient instead of a palliative patient.",
        document_order=204,
        coordinates="6,178.45,453.45,109.95,9.36;6,56.51,465.46,231.90,9.36;6,56.51,477.47,32.57,9.36",
    ),
    Text(
        content="With explicit attention to communication and spiritual care education, it is possible to better prepare students for working in the professional field.",
        document_order=205,
        coordinates="6,91.84,477.47,196.56,9.36;6,56.51,489.48,231.88,9.36;6,56.51,501.49,209.89,9.36",
    ),
    Text(
        content="The spiritual dimension of care deserves explicit attention in the medical curriculum.",
        document_order=206,
        coordinates="6,271.55,501.49,16.86,9.36;6,56.51,513.50,231.89,9.36;6,56.51,525.51,112.93,9.36",
    ),
    Text(
        content=", 2022 by guest.",
        document_order=207,
        coordinates="5,581.69,629.05,2.77,12.51;5,576.14,644.06,8.33,20.02;5,576.14,666.58,8.33,9.50;5,576.14,678.58,8.33,24.52",
    ),
    Text(
        content="Protected by http://spcare.bmj.com/",
        document_order=208,
        coordinates="5,576.14,705.60,8.33,38.52;5,576.14,746.62,8.33,9.50;5,576.14,490.99,8.33,88.53",
    ),
    Text(
        content="Original research",
        document_order=209,
        coordinates="6,60.50,24.52,85.87,9.48",
    ),
    Text(
        content="The eight learning tasks",
        document_order=210,
        coordinates="2,348.73,604.84,81.98,9.01",
    ),
    Text(
        content="The incorporated educational principles in the different learning tasks",
        document_order=211,
        coordinates="3,98.34,541.72,188.43,9.01;3,60.50,552.72,47.85,9.01",
    ),
    Text(
        content="Themes and quotes of the stakeholders this(authenticity, eds.)in so far that patients tell you a lot of stories.",
        document_order=212,
        coordinates="5,98.34,50.36,134.78,9.01;5,145.80,80.06,206.18,8.06",
    ),
    Text(
        content="So, in that sense, they are all very authentic stories and this is how patients present themselves to doctors'-I10'If you look at the learning tasks, you do see a clear structure.",
        document_order=213,
        coordinates="5,353.71,80.06,182.09,8.06;5,108.50,89.56,161.34,8.06;5,108.50,118.06,189.47,8.06",
    ),
    Text(
        content="From watching to an increasingly active role to eventually actually having a conversation with a patient, of course'-I8",
        document_order=214,
        coordinates="5,299.70,118.06,231.07,8.06;5,108.50,127.57,130.78,8.06",
    ),
    Text(
        content="We thank Judith Westen and Jimmy Frerejean for their support in designing these learning tasks.",
        document_order=216,
        coordinates="6,130.65,548.07,129.88,7.96;6,56.50,557.58,218.13,7.96",
    ),
    Text(
        content="We further thank the involved students, teachers and educational scientist.",
        document_order=217,
        coordinates="6,276.96,557.58,11.43,7.96;6,56.50,567.09,222.78,7.96;6,56.50,576.60,31.41,7.96",
    ),
    Text(
        content="Contributors DV and FW developed the learning tasks; JP and EN conducted the data collection.",
        document_order=218,
        coordinates="6,56.50,590.11,227.18,8.07;6,56.50,599.62,124.24,7.96",
    ),
    Text(
        content="JP, EN and FW interpreted the data.",
        document_order=219,
        coordinates="6,183.11,599.62,97.60,7.96;6,56.50,609.13,31.66,7.96",
    ),
    Text(
        content="JP drafted the manuscript; DV, MvdBvE and DD.",
        document_order=220,
        coordinates="6,90.53,609.13,179.27,7.96",
    ),
    Text(
        content="supervised the study process.",
        document_order=221,
        coordinates="6,56.50,618.64,105.25,7.96",
    ),
    Text(
        content="All authors have read and agreed to the final version of the manuscript.",
        document_order=222,
        coordinates="6,164.11,618.64,119.80,7.96;6,56.50,628.15,137.67,7.96",
    ),
    Text(
        content="Funding This work was supported by ZonMW (project number 80-84400-98-027).",
        document_order=223,
        coordinates="6,56.50,641.66,231.68,8.07;6,56.50,651.17,70.40,7.96",
    ),
    Text(
        content="Patient consent for publication Not required.",
        document_order=225,
        coordinates="6,56.50,678.18,164.07,8.07",
    ),
    Text(
        content="Board (NVMO-ERB file 2020.5.3).",
        document_order=227,
        coordinates="6,56.50,710.71,128.95,7.96",
    ),
    Text(
        content="Written consent was obtained from all participants.",
        document_order=228,
        coordinates="6,187.82,710.71,73.58,7.96;6,56.50,720.23,110.46,7.96",
    ),
    Text(
        content="The participants gave their permission to use anonymised quotes.",
        document_order=229,
        coordinates="6,169.32,720.23,97.51,7.96;6,56.50,729.74,137.92,7.96",
    ),
    Text(
        content="Provenance and peer review Not commissioned; externally peer reviewed.",
        document_order=230,
        coordinates="6,306.88,45.02,215.24,8.07;6,306.88,54.66,53.42,7.96",
    ),
    Text(
        content="Commercial (CC BY-NC 4.0) license, which permits others to distribute, remix, adapt, build upon this work noncommercially, and license their derivative works on different terms, provided the original work is properly cited, appropriate credit is given, any changes made indicated, and the use is noncommercial.",
        document_order=233,
        coordinates="6,306.88,109.36,214.63,7.96;6,306.88,118.49,195.94,7.96;6,306.88,127.63,220.30,7.96;6,306.88,136.77,231.89,7.96;6,306.88,145.91,230.06,7.96;6,306.88,155.04,44.63,7.96",
    ),
    Text(
        content="See: http:// creativecommons.",
        document_order=234,
        coordinates="6,353.87,155.04,105.68,7.96",
    ),
    Text(
        content="org/ licenses/ by-nc/ 4. 0/.",
        document_order=235,
        coordinates="6,459.54,155.04,73.63,7.96;6,306.88,164.18,9.45,7.96",
    ),
    Text(
        content="Jolien Pieters http:// orcid.",
        document_order=237,
        coordinates="6,306.88,191.46,94.21,7.96",
    ),
    Text(
        content="org/ 0000-0002-9327-3977",
        document_order=238,
        coordinates="6,401.10,191.46,98.73,7.96",
    ),
]

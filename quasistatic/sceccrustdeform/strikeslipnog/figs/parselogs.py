files = ["run_tet4_0500m_np1.log",
         "run_tet4_0500m_np2.log",
         "run_tet4_0500m_np4.log",
         "run_tet4_0500m_np8.log",
         "run_tet4_0500m_np16.log",
         "run_hex8_0500m_np1.log",
         "run_hex8_0500m_np2.log",
         "run_hex8_0500m_np4.log",
]
#         "run_hex8_0500m_np8.log",
#         "run_hex8_0500m_np16.log",
#         ]

stats = []
for filename in files:
    fin = open("../logs/2010jun/viscoelastic/%s" % filename, "r")
    lines = fin.readlines()

    total = 0.0
    compute = 0.0

    for line in lines:
        # Total
        indexBegin = 22
        indexEnd = 31
        record = "Time (sec):"
        if line[0:len(record)] == record:
            total = float(line[indexBegin:indexEnd])

        # Stages
        indexBegin = 21
        indexEnd = 31

        record = " 3: Reform Jacobian:"
        if line[0:len(record)] == record:
            fields = line.split()
            compute += float(line[indexBegin:indexEnd])

        record = " 4: Reform Residual"
        if line[0:len(record)] == record:
            fields = line.split()
            compute += float(line[indexBegin:indexEnd])

        record = " 5:           Solve"
        if line[0:len(record)] == record:
            fields = line.split()
            compute += float(line[indexBegin:indexEnd])

    stats.append({'filename': filename,
                  'total': total,
                  'compute': compute})

for s in stats:
    print s

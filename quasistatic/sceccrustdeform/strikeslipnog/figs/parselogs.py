files = ["run_tet4_0500m_np1.log",
         "run_tet4_0500m_np2.log",
         "run_tet4_0500m_np4.log",
         "run_tet4_0500m_np8.log",
         "run_tet4_0500m_np16.log",
         "run_hex8_0500m_np1.log",
         "run_hex8_0500m_np2.log",
         "run_hex8_0500m_np4.log",
         "run_hex8_0500m_np8.log",
         "run_hex8_0500m_np16.log",
         ]

stats = []
for filename in files:
    fin = open("../logs/2008nov25/%s" % filename, "r")
    lines = fin.readlines()

    total = 0.0
    compute = 0.0

    offset = 3
    for line in lines:
        # Events
        indexBegin = 29
        indexEnd = 39
        record = "PyLith main"
        if line[offset:offset+len(record)] == record:
            total = float(line[offset+indexBegin:offset+indexEnd])

        # Stages
        indexBegin = 21
        indexEnd = 31

        record = " 5: Reform Jacobian"
        if line[offset:offset+len(record)] == record:
            fields = line.split()
            compute += float(line[offset+indexBegin:offset+indexEnd])

        record = " 6: Reform Residual"
        if line[offset:offset+len(record)] == record:
            fields = line.split()
            compute += float(line[offset+indexBegin:offset+indexEnd])

        record = " 7:           Solve"
        if line[offset:offset+len(record)] == record:
            fields = line.split()
            compute += float(line[offset+indexBegin:offset+indexEnd])

    stats.append({'filename': filename,
                  'total': total,
                  'compute': compute})

for s in stats:
    print s

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
    fin = open("../logs/2008mar/%s" % filename, "r")
    lines = fin.readlines()

    total = 0.0
    distribute = 0.0

    indexBegin = 29
    indexEnd = 39
    for line in lines:
        record = "PyLith main"
        if line[0:len(record)] == record:
            total = float(line[indexBegin:indexEnd])
            print float(line[indexBegin:indexEnd])

        record = "Dist"
        if line[0:len(record)] == record:
            fields = line.split()
            distribute += float(line[indexBegin:indexEnd])
            print float(line[indexBegin:indexEnd])

    stats.append({'filename': filename,
                  'total': total,
                  'distribute': distribute})

for s in stats:
    print s

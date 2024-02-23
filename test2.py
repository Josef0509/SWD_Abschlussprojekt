from c_benotung import percentageTOGrade, gradeTOPercentage


for i in range(1, 6):
    print(f"Grade: {i} -> Percentage: {gradeTOPercentage(i)}")

for i in range(0, 101, 1):
    print(f"Percentage: {i} -> Grade: {percentageTOGrade(i)}")


print(percentageTOGrade(0.928))
#!/usr/bin/python
from math import sqrt

def isPalindrome(value):
    value = str(value)
    temp = value[::-1]
    for n in range(0, len(value)):
        if value[n] != temp[n] :
            return 1
    return 0

def euler_55():
    lychrel = 0
    for n in range(11, 10000):
        count = 0
        isPal = 1
        revn = str(n)[::-1]
        total = int(n) + int(revn)
        while (count < 50 and  isPal != 0):

            isPal = isPalindrome(total)

            #print "count : %d num %d isPal %d"%(count,total, isPal)
            if isPal == 1:
                count += 1
                revn= str(total)[::-1]
                total = int(total) + int(revn)
        if isPal == 1:
            lychrel += 1
            print("count <%d> num <%d> revn <%s> total<%s> isPal %d lychrel %d"%(count, n, revn, total, isPal, lychrel))

def isLeap(year):
    if ((year % 400 == 0) or (year % 100 != 0 and year % 4 == 0)):
        return 0
    else:
        return 1
def euler_19_sundays():
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    wk_days = ["Sun","Mon","Tue","Wed","Thur","Fri","Sat"]
    month_days=[31,28,31,30,31,30,31,31,30,31,30,31]
    month = 0
    sun_count = 0
    for year in range(1900, 1901):
        leap = isLeap(year)
        if leap == 0:
            month_days[1] = 29
        for days in month_days:
            for day in range(1,days +1):
                d = day % 7
                if d == 0:
                    sun_count += 1
                    print("date: %d day is : %s month: %s year %d"%(day,wk_days[d],months[month], year))
            month += 1
        month = month % 12
    print("number of sundays: %d"%sun_count)
    return 0

def euler_56():
    sum = 0
    max = 0
    for a in range(1,100):
        for b in range(1,100):
            c = a ** b
            sc = str(c)
            sum = 0
            for w in sc:
                sum += int(w)
            if (max < sum ):
                max = sum
    print("max is %d"%max)

def fs():
    a,b,c=0,1,0
    while b < 1000000:
        if b %2 == 0:
            c +=b
        a,b=b,a+b
    print (c)
def isPrime(value):
    if value < 2:
        return 1
    elif value == 2:
        return 0
    elif value %2 == 0:
        return 1
    else:
        for n in range(3, int(value**0.5)+2,2):
            if value % n == 0:
                return 1
        return 0
def euler_3(value):
    alist = []
    i =2
    while ( i <= value ) :
        if ( value % i == 0) :
            if (isPrime(i) == 0 ):
                print("%d -- %d  is prime %d" % (value, i, isPrime(i)))
                alist.append(i)
        i += 1
    for item in alist:
        print(item)
def euler_7(ulimit):
    i = 2
    count = 1
    while (count <= ulimit):
        if (isPrime(i) == 0 ):
            count += 1
            print("%d the value is %d" %(count, i))
        i += 1
    print ("%d the value is %d"%(ulimit, i))
def euler_10(ulimit):
    i = 2
    sum = 0
    while (i < ulimit):
        if (isPrime(i) == 0):
            sum += i
        if ( i % 2000 == 0):
            print("%d sum is %d"%(i, sum))
        i += 1
    print("sum of all primes below %d is %d"%(ulimit, sum))
def euler_14(ulimit):
    count = 0
    num = ulimit
    tmp = 0
    while num > 1 :
        if (num %2 == 0 ):
            num /= 2
            count += 1
        else:
            num = 3* num +1
            count += 1
    return count
def euler_16():
    ulimit = 1000
    num = 2**ulimit
    lnum = str(num)
    print ("lnum is %s"%lnum)
    sum = 0
    for n in lnum:
        sum += int(n)
    print ("Total of %s is %d"%(lnum, sum) )

def euler_20(value):
    sum = 1;
    for i in range (1 , value+1):
        sum *= i
    print ("sum is %d" %sum)
    sum = str(sum)
    total = 0
    for n in range(0, len(sum)):
        print( "%d %s"%( n,sum[n]))
        total += int(sum[n])
    print("total : %d"%total)
    return sum
def euler_21(value):
    sum = 0
    total1 = 0
    total2 = 0
    for n in range(1, value):
        if (value %n == 0 ):
            total1 += n
    value1 = total1
    total2 =0
    for n in range(1, value1):
        if (value1 %n == 0 ):
            total2 += n
    if (value == total2 and total1 != total2):
        sum = sum + total1 + total2

    if sum > 0 :
        print ("value1 is : %d total1 %d"%(value,total1))
        print ("value2 is: %d total2 %d"%(value1,total2))
        print ( "sum of amicable numbers is :%d"%sum)
    return sum
def euler_22(filename):
    f = open(filename, 'r')
    lines = f.read();
    f.close()
    alist = lines.split(",")
    blist = []
    for word in alist:
        word = word.replace("\"", "")
        blist.append(word)
    blist.sort()
    for word in blist:
        print (word)
    alphalist=['0','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    rank = 1
    gtotal = 0
    for word in blist:
        total =0
        for w in word:
            total = total + alphalist.index(w)
        print ( "total  of word <%s> is : %d"% (word,total))
        gtotal += (total *rank)
        rank += 1
    print ("grand total is : %d"%gtotal)

def fibonacci_25():
    a= 0
    b=1
    length = 0
    tmp = 0
    count = 1
    while 1 : 
        tmp = a
        a = b
        b = tmp + b
        length = len(str(b))
        count += 1
        if length == 1000:
            break
    print(  "fibonacci_25 %d is :%d"%( count, length))
def euler_30():
    n = 2
    count = 0
    sum  = 0
    while 1:
        total = 0
        for i in str(n):
            total += int(i) ** 5
        if total == n :
            print( "n %d total %d "% (n,total))
            count += 1
            sum += total
            print ("Sum of all the numbers is : %d"%(sum))
        n += 1
        if count == 6:
            break
    print("Sum of all the numbers is : %d"%(sum))
def triangle_word(filename):
    f = open(filename, "r")
    words = f.read()
    f.close()
    wordlist = words.split(",")
    alphalist=['0','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    count = 0
    max = 0
    tr_num = []
    for x in range(1, 100):
        n = x * (x+1)/2
        tr_num.append(n)
    for word in wordlist:
        word = word.replace("\"", "")
        total = 0
        for w in word:
            total += alphalist.index(w)

        triangle_num = tr_num.index(total)
        print("total %d and triangle_num %d "%(total, triangle_num))
        if (triangle_num >= 0 ):
            print ("Total %d  for word %s "%(total, word))
            count += 1
    print( "total triangle words are : %d max %d"%(count, max))
             
def euler_48():
    total = 0
    for n in range(1, 1001):
        total += (n **n)
    print( "total is : %d"%(total))
def euler_29(value): 
    alist = []
    for a in range (2, value +1):
        for b in range(2, value +1):
            c = a ** b;
            print( a ** b,)
            if c not in alist:
                alist.append(c)
        print( "\n")
    print( len(alist))
def euler_8():
    num = 7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450 
    max = 0
    num = str(num)
    count = 0
    for n in num:
        total = 1
        print( "n %s"% n)
        for i in range(0,5):
            if count +i == len(num):
                break
            total *= int(num[count +i])
            print( total,)

        print( "\n")
        if max < total:
            max = total
        count += 1
    print( max)
def euler_13():
    nums= [37107287533902102798797998220837590246510135740250,46376937677490009712648124896970078050417018260538,74324986199524741059474233309513058123726617309629,91942213363574161572522430563301811072406154908250,23067588207539346171171980310421047513778063246676,89261670696623633820136378418383684178734361726757,28112879812849979408065481931592621691275889832738,44274228917432520321923589422876796487670272189318,47451445736001306439091167216856844588711603153276,70386486105843025439939619828917593665686757934951,62176457141856560629502157223196586755079324193331,64906352462741904929101432445813822663347944758178,92575867718337217661963751590579239728245598838407,58203565325359399008402633568948830189458628227828,80181199384826282014278194139940567587151170094390,35398664372827112653829987240784473053190104293586,86515506006295864861532075273371959191420517255829,71693888707715466499115593487603532921714970056938,54370070576826684624621495650076471787294438377604,53282654108756828443191190634694037855217779295145,36123272525000296071075082563815656710885258350721,45876576172410976447339110607218265236877223636045,17423706905851860660448207621209813287860733969412,81142660418086830619328460811191061556940512689692,51934325451728388641918047049293215058642563049483,62467221648435076201727918039944693004732956340691,15732444386908125794514089057706229429197107928209,55037687525678773091862540744969844508330393682126,18336384825330154686196124348767681297534375946515,80386287592878490201521685554828717201219257766954,78182833757993103614740356856449095527097864797581,16726320100436897842553539920931837441497806860984,48403098129077791799088218795327364475675590848030,87086987551392711854517078544161852424320693150332,59959406895756536782107074926966537676326235447210,69793950679652694742597709739166693763042633987085,41052684708299085211399427365734116182760315001271,65378607361501080857009149939512557028198746004375,35829035317434717326932123578154982629742552737307,94953759765105305946966067683156574377167401875275,88902802571733229619176668713819931811048770190271,25267680276078003013678680992525463401061632866526,36270218540497705585629946580636237993140746255962,24074486908231174977792365466257246923322810917141,91430288197103288597806669760892938638285025333403,34413065578016127815921815005561868836468420090470,23053081172816430487623791969842487255036638784583,11487696932154902810424020138335124462181441773470,63783299490636259666498587618221225225512486764533,67720186971698544312419572409913959008952310058822,95548255300263520781532296796249481641953868218774,76085327132285723110424803456124867697064507995236,37774242535411291684276865538926205024910326572967,23701913275725675285653248258265463092207058596522,29798860272258331913126375147341994889534765745501,18495701454879288984856827726077713721403798879715,38298203783031473527721580348144513491373226651381,34829543829199918180278916522431027392251122869539,40957953066405232632538044100059654939159879593635,29746152185502371307642255121183693803580388584903,41698116222072977186158236678424689157993532961922,62467957194401269043877107275048102390895523597457,23189706772547915061505504953922979530901129967519,86188088225875314529584099251203829009407770775672,11306739708304724483816533873502340845647058077308,82959174767140363198008187129011875491310547126581,97623331044818386269515456334926366572897563400500,42846280183517070527831839425882145521227251250327,55121603546981200581762165212827652751691296897789,32238195734329339946437501907836945765883352399886,75506164965184775180738168837861091527357929701337,62177842752192623401942399639168044983993173312731,32924185707147349566916674687634660915035914677504,99518671430235219628894890102423325116913619626622,73267460800591547471830798392868535206946944540724,76841822524674417161514036427982273348055556214818,97142617910342598647204516893989422179826088076852,87783646182799346313767754307809363333018982642090,10848802521674670883215120185883543223812876952786,71329612474782464538636993009049310363619763878039,62184073572399794223406235393808339651327408011116,66627891981488087797941876876144230030984490851411,60661826293682836764744779239180335110989069790714,85786944089552990653640447425576083659976645795096,66024396409905389607120198219976047599490197230297,64913982680032973156037120041377903785566085089252,16730939319872750275468906903707539413042652315011,94809377245048795150954100921645863754710598436791,78639167021187492431995700641917969777599028300699,15368713711936614952811305876380278410754449733078,40789923115535562561142322423255033685442488917353,44889911501440648020369068063960672322193204149535,41503128880339536053299340368006977710650566631954,81234880673210146739058568557934581403627822703280,82616570773948327592232845941706525094512325230608,22918802058777319719839450180888072429661980811197,77158542502016545090413245809786882778948721859617,72107838435069186155435662884062257473692284509516,20849603980134001723930671666823555245252804609722,53503534226472524250874054075591789781264330331690] 
    total = 0
    for n in nums:
        total += n
    print( total)
def euler_9():
    prod = 0
    a = 1
    b = 2
    c = 3
    sum = 0
    while sum != 1000:
        for c in range(1, 1000):
            for  b in range(1,1000):
                if b > c:
                    break
                for a in range(1,1000):
                    if a > b or b > c:
                        break
                    a2 = a**2
                    b2 = b**2
                    c2 = c**2
                    if (a2 + b2) == c2:

                        sum = a + b +c 
                        print( "a : %d b: %d c: %d total: %d "%(a,b,c,sum))
                        if sum == 1000:
                            prod = a * b * c
                            print( "prod %d"% prod)
                            return prod


    print( prod)
def isTriangle_num(tnum):
    n = 1
    while 1:
        tmp = n * (n+1) /2
        n += 1
        if tmp == tnum:
            return 0
        elif tmp > tnum:
            return 1

    return 1
def triangle_word_euler_42(filename):
    alphalist=['0','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    f = open(filename, "r")
    lines = f.read()
    f.close()
    blist = []
    wordlist = lines.split(",")
    count = 0
    for word in wordlist:
        word = word.replace("\"", "")
        blist.append(word)
    for word in blist:
        sum = 0
        for w in word:
            sum += alphalist.index(w)
        is_tri = isTriangle_num(sum)
        if is_tri == 0:
            count += 1
    print( "Number of words %d"%(count))
def triangle_num_euler_12():
    n =1
    count = 0
    tnum = 2
    while count  < 500:
        tnum = n * (n+1) /2
        divs = divisorGenerator(tnum)
        count=sum(1 for x in divs)
        if count > 100:
            print( "tnum %d count %d"%(tnum, count))

        n +=1
    print( "tnum :%d"%tnum)
def divisorGenerator(n):
    for i in xrange(1, sqrt(n) +1):
        if n%i == 0:
            yield i
            yield n/i

if __name__ == '__main__': 
    print( "Hello World")
    #value = 13000000
    #n = isPrime(value)
    #print " %d is prime %d"%(value, n)
    #euler_3(600851475143) 
    #euler_7(10001)
    #euler_10(2000000)
    """
    tmp = 0
    count = 0
    for x in range(13,1000000):
        count = euler_14(x)
        if tmp < count:
            tmp = count
            print( "count is %d for %d"%(count, x))
    """
    euler_3 (20) 
    #euler_20(100)
    #sum = 0
    #for n in range(1,10000):
    #    sum += euler_21(n)
    #print "grand sum is : %d"%sum
    #euler_22("names.txt")
    #fibonacci_25()
    #euler_30()
    #euler_48()
    #triangle_word("words.txt")
    #euler_29(100)
    #euler_8()
    #euler_13()
    #euler_9()
    #triangle_num_euler_12()
    #triangle_word_euler_42("words_triangle.txt")
    #euler_56()
    #euler_55()
    #euler_19_sundays()

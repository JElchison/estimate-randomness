# estimate-randomness
Estimate the randomness of a sequence of integers meant to model a discrete distribution

A perfectly random discrete distribution will model a [discrete uniform distribution](https://en.wikipedia.org/wiki/Discrete_uniform_distribution), having a maximum entropy of `ln(n)`.  This script attempts to estimate the amount of randomness of a sequence of integers in that distribution.

It does so by first calculating the [entropy](https://en.wikipedia.org/wiki/Entropy_(information_theory)) of the data set.  Then, it repeats the process, but replacing the data set with its differential complement.  Item 5 in the list is replaced by the difference between item 5 and 4.  This is to prevent a sequence like `1 2 3 4 5` from being considered random.  While perfectly uniform, it has maximal entropy; however, it should not be considered random.

The value reported as estimated_randomness is the minium value of the entropy of the data set and the entropy of its differential complement.

    * 0.0 means not random
    * 1.0 means highly random

With a large enough data set, the reported estimated_randomness value should approximate 1.0.


## Usage

```
./estimate-randomness.py [input_file [(lower_bound) (upper_bound)]]

input_file - Place from which to read list of integers.  Can be '-' for stdin.
             Defaults to '-' for stdin.
             
lower_bound - Lowest integer value expected to be seen in input_file (inclusive).
              Defaults to mininum of data set.
              Useful for detecting when items at beginning and end of range are not used.
              
upper_bound - Highest integer value expected to be seen in input_file (inclusive).
              Defaults to maximum of data set.
              Useful for detecting when items at beginning and end of range are not used.
```

## Examples
Input sequence = 1 1 1 1 1
```
$ for NUM in 1 1 1 1 1; do echo $NUM; done | ./estimate-randomness.py
No range provided.  Not counting any values with frequency of 0.
Using total range of 1.

max_possible_entropy = 0.0

overall_entropy = 0.0
overall_randomness = 0

differential_entropy = 0.0
differential_randomness = 0

estimated_randomness = 0
```

Input sequence = 1 2 3 4 5
```
$ for NUM in 1 2 3 4 5; do echo $NUM; done | ./estimate-randomness.py
No range provided.  Not counting any values with frequency of 0.
Using total range of 5.

max_possible_entropy = 1.60943791243

overall_entropy = 1.60943791243
overall_randomness = 1.0

differential_entropy = 0.0
differential_randomness = 0

estimated_randomness = 0
```

Input sequence = set of 2048 integers (between 0 and 255) from /dev/urandom
```
$ for HEX in $(head -c 2048 /dev/urandom | xxd -p | sed -r 's/[0-9a-f]{2}/\0 /g' | tr -d '\n'); do echo $((16#$HEX)); done | ./estimate-randomness.py - 0 255
Using total range of 256.

max_possible_entropy = 5.54517744448

overall_entropy = 5.48412677091
overall_randomness = 0.988990312

differential_entropy = 5.47797110335
differential_randomness = 0.987880218118

estimated_randomness = 0.987880218118
```

Input sequence = set of source port numbers used by your operating system
```
$ tcpdump -i eth0 -w mycap.pcap
$ bro -r mycap.pcap
$ awk '{print $4}' conn.log | egrep '[0-9]+' | ./estimate-randomness.py - 1024 65535
Using total range of 65403.

max_possible_entropy = 11.088323408

overall_entropy = 3.10649690465
overall_randomness = 0.280159298241

differential_entropy = 3.2913361528
differential_randomness = 0.296829018392

estimated_randomness = 0.280159298241
```

This last example shows a low estimated_randomness since the pcap only contains a few connections (thus, the distribution is considered sparse in the range 1024-65535).

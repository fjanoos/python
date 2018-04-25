#!/usr/bin/python

# Program to generate a concordance list from the text formatted as:
#   word_1 { sentence_number_1 : occurence_count, sentence_number_2: occurence_count, ... }
#   word_2 { sentence_number_1 : occurence_count, sentence_number_2: occurence_count, ... }
# Note: A sentence is defined as starting with a word with its first letter capitalized
#       and ending with a period. In case this rule is not respected, sentence counts will
#       be incorrect


from optparse import OptionParser
import sys

def computeConcordance(file_input, verbose_flag = True):
    
    word_dictionary = {};
    strip_list = ',:;`\'"()[]{}'
    
    sentence_number = 1; #keep track of sentence
 
    # read the file and tokenize
    word_list = file_input.read().split();
    curr_word = word_list[0];
    
    for next_word in word_list[1:]:
        inc_count  = 0;               
        # test for a new sentence
        if curr_word.endswith('.') and next_word.istitle():
            inc_count  = 1;               
            #  strip out the trialing .
            curr_word = curr_word.rstrip('.');
            if verbose_flag:
                print 'reading sentence #%d ' % sentence_number;
           
        # convert word to lower-case and strip of certain characters            
        word_ = curr_word.lower().strip(strip_list);
            
        if word_ in word_dictionary.keys():
            if sentence_number in word_dictionary[word_].keys():
                word_dictionary[word_][sentence_number] += 1;
            else:
                word_dictionary[word_][sentence_number] = 1;
        else:
            word_dictionary[word_] = {sentence_number:1};               

        curr_word = next_word;
        sentence_number += inc_count;    

    # process the last word - remove the trailing fullstop
    word_ = curr_word.lower().strip(strip_list+'.');
    if word_ in word_dictionary.keys():
        if sentence_number in word_dictionary[word_].keys():
            word_dictionary[word_][sentence_number] += 1;
        else:
            word_dictionary[word_][sentence_number] = 1;
    else:
        word_dictionary[word_] = {sentence_number:1};         
        
    # do a cleanup
    word_list = word_dictionary.keys();       

    for word in word_list:
        if word+'.' in word_list:
            cc_word = word_dictionary[word+'.'];
            for (k,v) in cc_word.iteritems():
                if k in word_dictionary[word]:
                    word_dictionary[word][k] += v;
                else:
                    word_dictionary[word][k] = v;
            del word_dictionary[word+'.']
    return word_dictionary;

if __name__ == "__main__":
    usage = \
'''  %prog [options] input_filename 
           Prints the concordance list of the given text file ''';
    option_parser = OptionParser(usage)  
    option_parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False) ;

    (options, args) = option_parser.parse_args()

       
    if len(args) != 1:
        #option_parser.error("incorrect number of arguments")
        option_parser.print_help();
        sys.exit();
       
    
    try:
        file_input = open(args[0], 'r')
    except IOError:
        print 'cannot open '+ args[0]
    else:
        if options.verbose:
            print 'generating concordance for '+args[0];
            
        condcordance_list = computeConcordance(file_input, options.verbose);
        word_list = condcordance_list.keys();
        word_list.sort();
        for word in word_list:
            print '%25s'%word, ' : ', condcordance_list[word]



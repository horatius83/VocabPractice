import Data.List hiding (words)
import System.Random
import System.IO
import System.Directory
import Prelude hiding (words)
import Data.Ord ()

data Vocab = NewWord String | Word String Bool deriving (Eq, Read, Show) 
type VocabList = [Vocab]

-- Really inefficient shuffling algorithm
shuffle :: [a] -> Int -> [a]
shuffle [] _ = [] 
shuffle lst seed = 
    let r = mkStdGen seed
    	len = length lst
        rands = take len (randoms r :: [Double])
        comparer (_,x) (_,y) = compare x y
        tuples = zip lst rands
        sortedTuples = sortBy comparer tuples
    in [j | (j,_) <- sortedTuples]

-- Shuffle a list
shuffleM :: [a] -> IO [a]
shuffleM lst = do
    r <- newStdGen
    let lst' = shuffle lst $ head (randoms r :: [Int])
    return lst'

-- Given a list of strings, convert to a VocabList
createNewVocabList :: [String] -> VocabList
createNewVocabList words = [NewWord word | word <- words]

-- Get the string value of a given vocabulary item
getWord :: Vocab -> String
getWord (NewWord x) = x
getWord (Word x _) = x

-- Remove learned words, update updated words (make them True), shuffle and return
s :: [String] -> [String] -> IO VocabList -> IO VocabList
s learned updated lst = do
    vocab <- lst
    let allChanged = learned ++ updated
        toWord x = case x of Word y True -> Word y False
                             y -> y
        unchanged = filter (\x -> getWord x `notElem` allChanged) $ map toWord vocab
    shuffleM $ unchanged ++ [Word x True | x <- updated]

-- Add words to the list
addWords :: [String] -> IO VocabList -> IO VocabList
addWords newWords vocabList = do
    lst <- vocabList
    let lst' = [NewWord x | x <- newWords] ++ lst
    return lst'

-- Print an item in the list
printItem :: Vocab -> IO ()
printItem word = do
        case word of
            (NewWord y) -> putStrLn y
            (Word y True) -> putStrLn $ y ++ " *"
            (Word y False) -> putStrLn y 


-- Print the list
pl :: IO VocabList -> IO ()
pl vocabList = do
    lst <- vocabList
    mapM_ printItem lst

-- Print the ones that we got wrong
wrongAnswers :: [String] -> IO VocabList -> IO VocabList
wrongAnswers corrected vocab = do
    vList <- vocab
    let isCorrectOrInList x = case x of Word w v -> v || elem w corrected 
                                        NewWord w -> w `elem` corrected 
        filteredWords = [x | x <- vList, not (isCorrectOrInList x)]
    shuffleM filteredWords    

-- Read the vocabulary list
readVocabList :: String -> IO [Vocab]
readVocabList filename = do
    inFile <- openFile filename ReadMode
    contents <- hGetContents inFile
    contents `seq` hClose inFile
    let lst = lines contents
        vocab = [read x :: Vocab | x <- lst]
    return vocab

-- Write the vocabulary list
writeVocabList :: String -> IO [Vocab] -> IO ()
writeVocabList filename vocabList = do
    handle <- openFile filename ReadMode
    (tempName, tempHandle) <- openTempFile "." "temp"
    vocab <- vocabList
    let txt = unlines $ map show vocab
    hPutStr tempHandle txt
    hClose handle
    hClose tempHandle
    removeFile filename
    renameFile tempName filename

-- for convenience
readVocab :: IO VocabList
readVocab = readVocabList "vocab.txt"

writeVocab :: IO VocabList -> IO ()
writeVocab = writeVocabList "vocab.txt" 

raf :: [String] -> [String] -> IO [Vocab]
raf correctWords updatedWords = do
    let vocabFile = "vocab.txt"
        vocab = readVocabList vocabFile 
        vocab' = s correctWords updatedWords vocab
    writeVocabList vocabFile vocab'
    vocab'

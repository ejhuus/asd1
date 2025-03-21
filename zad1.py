from typing import Any, Union

# Pomocnicza funkcja, dodająca spację na początku każdej linijki w napisie.
def indent(s: str) -> str:
    return '\n'.join(' '+line for line in s.splitlines())


class Leaf:
    # Pola poniżej należą do instancji, nie do klasy! (nie są statyczne)
    # Gdyby nie było typów, zmienna zadeklarowana tutaj byłaby statyczna.
    value: Any
    size: int
    
    def __init__(self, value: Any):
        self.value = value
        self.size = -1

    # Prosta pomocnicza funkcja do wypisywania (pod)drzewa (można napisać własną, bardziej czytelną); również w RegBinNode.
    def __str__(self):
        return f'{self.value} (size: {self.size})\n'

    #Funkcja ustawiająca prawidłowy size dla liścia
    def calc_node(self):
        self.size = 1
        return self.size


class RegBinNode:
    # Pola poniżej należą do instancji, nie do klasy! (nie są statyczne)
    value: Any
    left: Union['RegBinNode',Leaf]
    right: Union['RegBinNode',Leaf]
    size: int

    def __init__(self,
                 value: Any,
                 left: Union['RegBinNode',Leaf], 
                 right: Union['RegBinNode',Leaf]):
        self.value = value
        self.left = left
        self.right = right
        self.size = -1
    
    def __str__(self):
        return f'{self.value} (size: {self.size})\n{indent(str(self.left))}\n{indent(str(self.right))}'

    #Rekurencyjnie działająca funkcja działająca na węźle.
    def calc_node(self):
        result = 1
        if self.left:
            result += self.left.calc_node()
        if self.right:
            result += self.right.calc_node()
        self.size=result
        return self.size


class RegBinTree:
    # Pole "root" należy do instancji, nie do klasy! (nie jest statyczne)
    root: RegBinNode|Leaf|None

    def __init__(self, node: RegBinNode|Leaf|None = None):
        self.root = node
    
    def calculate_sizes(self):
        # TODO: uzupełnij tę metodę (możesz deklarować dodatkowe metody tutaj, w PosBinNode lub globalnie).
        if self.root is None:
            return None
        #Zacznij rekurencje od korzenia.
        self.root.calc_node()
        pass

    # Funkcja znajdująca centroid w drzewie.
    def find_centroid(self) -> RegBinNode|Leaf|None:
        # Funkcja zwraca None jeśli drzewo jest puste.
        if self.root is None:
            return None
        # Funkcja wylicza maksymalną możliwą wielkość każdego z poddrzew powstałych po usunięciu centroidu.
        max_size = int(self.root.size / 2)
        # Rekurencyjna funkcja pomocnicza. Dla wskazanego węzła sprawdza, czy któreś z jego poddrzew (o ile istnieją) jest rozmiaru większego niż max_size.
        # Jeśli tak (może być takie co najwyżej jedno), to oznacza, że centroid musi znajdywać się w tym poddrzewie, zatem rekurencja zwraca wynik po wywołaniu
        # siebie dla tego poddrzewa. Jeśli nie ma poddrzewa o takim rozmiarze, to rekurencja zwraca wskazany węzeł jako szukany centroid.
        def find_node(node: RegBinNode|Leaf) -> RegBinNode|Leaf:
            if type(node) is RegBinNode:
                if type(node.left) is not None and node.left.size > max_size:
                    return find_node(node.left)
                if type(node.right) is not None and node.right.size > max_size:
                    return find_node(node.right)
            return node
        # Funkcja zwraca wynik po wywołaniu rekurencji pomocniczej na korzeniu. Ponieważ rekurencja zaczyna się od korzenia, to jeśli żadne z poddrzew
        # nie będzie większe od max_size, korzeń będzie centroidem. W przeciwnym wypadku rekurencja wywoła się od poddrzewa, w którym centroid
        # musi się znajdować, zatem rekurencja zawsze znajdzie centroid drzewa.
        # Rekurencja może wywoływać siebie jedynie w dół drzewa, a więc nie zostanie wywołana więcej razy, niż wynosi jego wysokość.
        return find_node(self.root)

    def __str__(self):
        return '(Empty tree)' if self.root is None else str(self.root)

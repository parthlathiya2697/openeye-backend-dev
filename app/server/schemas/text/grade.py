from typing import Optional
from pydantic import BaseModel

class Grade(BaseModel):
    text: str

    word_repetition_weight : Optional[float] = 0.1
    clearity_weight : Optional[float] = 0.5
    coherance_weight : Optional[float] = 0.1
    grammer_weight : Optional[float] = 0.1
    word_meaning: Optional[float] = 0.1

    class Config:
        schema_extra = {
            "example": {
                "text": "I was go to the school tomorrow",
            }
        }

class SEOGrade(BaseModel):

    topic: str
    text: str
    num_pages: int = 10

    class Config:
        schema_extra = {
            "example": {
                "topic": "How to make good sandwitches",
                "text": "1: Spread Out\nSandwich spreads add flavor but also perform the essential task of lending moisture and sometimes creaminess to sandwiches. Mustard and mayo are the familiar standbys, but don’t stop there. It’s well worth experimenting with the following: vinaigrettes, pestos, BBQ sauces, chutneys, and salsas.\n2: Use the Right Bread\n\nChoose bread appropriate to the sandwich you’re making. Pair moist fillings with soft, fluffy breads and you’ve got a recipe for a sponge, not a sandwich. As a general rule, the moister the filling the drier and denser the bread should be. A good, thick crust helps, too. Swap in large flour tortillas, if you like, for moist fillings. They keep ingredients in check and maintain their integrity much better than many breads.\n\n3: Choose To-Go Toppings\nWe love lettuce and tomato in sandwiches. They lend moisture, crunch and freshness and provide a wonderful foil for heavy, rich ingredients. They are, however, almost entirely water, and thus over extended periods are prone to wilting and, worse, making bread soggy. Luckily there are plenty of vegetables that offer all the benefits of lettuce and tomato without the drawbacks. In place of sliced tomatoes, for instance, try giving roasted peppers. (It helps if you first blot the peppers dry with a paper towel). Instead of lettuce, experiment with other vegetables, like sliced fennel, spinach, shredded cabbage, or cucumber.\n\n4: Stave Off Sogginess\n\nSpread mayo, butter or cream cheese all the way to the edges of each slice of bread to create a seal against wet sandwich fillings. Also, try packing high moisture ingredients, like tomatoes, pickles, and cucumbers, separately. Just add them to the sandwich when you’re ready to eat. Toasting the bread can help, too.\n5: Take the Edge Off Onions\n\nOnions can give sandwiches a welcome bite but often must be tamed a bit to be enjoyed raw. There are two effective ways to take some of the edge off sliced onions: Either soak thinly sliced onions in ice water for 20 minutes or so. Then drain and blot dry. (This method adds crispness.) Or toss sliced onions with a generous sprinkling of kosher salt. Wait a few minutes. Rub salt into the onions, rinse, drain.",
                "num_pages": "10",
            }
        }
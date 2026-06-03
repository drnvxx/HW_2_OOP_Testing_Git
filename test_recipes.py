from recipes import Ingredient
import pytest

# 2.1

def test_ingredient_creation():
    ing = Ingredient("Сахар", 150.0, "г")
    assert ing.name == "Сахар"
    assert ing.quantity == 150.0
    assert ing.unit == "г"


def test_ingredient_str():
    ing = Ingredient("Мука", 500.0, "г")
    assert str(ing) == "Мука: 500.0 г"


def test_ingredient_eq():
    ing1 = Ingredient("Соль", 10.0, "г")
    ing2 = Ingredient("Соль", 25.0, "г")
    assert ing1 == ing2

    ing3 = Ingredient("Перец", 10.0, "г")
    assert ing1 != ing3

    ing4 = Ingredient("Соль", 10.0, "кг")
    assert ing1 != ing4


from recipes import Recipe

#   2.2

def test_recipe_creation():
    ing1 = Ingredient("Картофель", 5.0, "шт")
    ing2 = Ingredient("Соль", 10.0, "г")

    recipe = Recipe("Пюре", [ing1, ing2])

    assert recipe.title == "Пюре"
    assert len(recipe.ingredients) == 2
    assert recipe.ingredients[0] == ing1
    assert recipe.ingredients[1] == ing2


def test_add_ingredient():
    recipe = Recipe("Сладкий чай")

    ing1 = Ingredient("Сахар", 10.0, "г")
    recipe.add_ingredient(ing1)

    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == 10.0

    ing2 = Ingredient("Сахар", 5.0, "г")
    recipe.add_ingredient(ing2)

    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == 15.0


def test_recipe_scale():
    ing = Ingredient("Мука", 100.0, "г")
    recipe = Recipe("Пирог", [ing])

    scaled_recipe = recipe.scale(2.5)

    assert scaled_recipe is not recipe
    assert recipe.ingredients[0].quantity == 100.0
    assert scaled_recipe.ingredients[0].quantity == 250.0

    with pytest.raises(ValueError):
        recipe.scale(0)

    with pytest.raises(ValueError):
        recipe.scale(-2.0)


def test_recipe_len():
    ing1 = Ingredient("Вода", 1.0, "л")
    ing2 = Ingredient("Заварка", 5.0, "г")

    recipe = Recipe("Чай", [ing1, ing2])

    assert len(recipe) == 2


from recipes import ShoppingList

#  2.3

def test_shopping_list_add_recipe():
    ing = Ingredient("Молоко", 1.0, "л")
    recipe = Recipe("Каша", [ing])

    shopping_list = ShoppingList()

    shopping_list.add_recipe(recipe, 2.0)

    assert len(shopping_list._items) == 1
    assert shopping_list._items[0][0].name == "Молоко"
    assert shopping_list._items[0][0].quantity == 2.0
    assert shopping_list._items[0][1] == "Каша"

    with pytest.raises(ValueError):
        shopping_list.add_recipe(recipe, 0)

    with pytest.raises(ValueError):
        shopping_list.add_recipe(recipe, -1.5)


def test_shopping_list_remove_recipe():
    ing = Ingredient("Яйцо", 2.0, "шт")
    recipe = Recipe("Омлет", [ing])

    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 1.0)

    shopping_list.remove_recipe("Омлет")

    assert len(shopping_list._items) == 0

    shopping_list.remove_recipe("Несуществующий рецепт")


def test_shopping_list_get_list():
    ing1 = Ingredient("Сыр", 100.0, "г")
    recipe1 = Recipe("Пицца", [ing1])

    ing2 = Ingredient("Сыр", 50.0, "г")
    recipe2 = Recipe("Бутерброд", [ing2])

    shopping_list = ShoppingList()

    shopping_list.add_recipe(recipe1, 1.0)
    shopping_list.add_recipe(recipe2, 2.0)

    ing3 = Ingredient("Абрикос", 1.0, "шт")
    recipe3 = Recipe("Десерт", [ing3])

    shopping_list.add_recipe(recipe3, 1.0)

    final_list = shopping_list.get_list()

    assert len(final_list) == 2

    assert final_list[0].name == "Абрикос"
    assert final_list[1].name == "Сыр"

    assert final_list[1].quantity == 200.0


def test_shopping_list_add_operator():
    ing1 = Ingredient("Яблоко", 2.0, "шт")
    recipe1 = Recipe("Пирог", [ing1])

    sl1 = ShoppingList()
    sl1.add_recipe(recipe1, 1.0)

    ing2 = Ingredient("Груша", 3.0, "шт")
    recipe2 = Recipe("Компот", [ing2])

    sl2 = ShoppingList()
    sl2.add_recipe(recipe2, 1.0)

    combined = sl1 + sl2

    assert combined is not sl1
    assert combined is not sl2
    assert len(combined._items) == 2

    assert len(sl1._items) == 1
    assert len(sl2._items) == 1
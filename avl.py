""" AVL Tree implemented on top of the standard BST. """

__author__ = 'Alexey Ignatiev, modified by Ze Chong, Daniel Ding and Maily Butel'
__docformat__ = 'reStructuredText'

from bst import BinarySearchTree
from typing import TypeVar, Generic
from node import AVLTreeNode

K = TypeVar('K')
I = TypeVar('I')


class AVLTree(BinarySearchTree, Generic[K, I]):
    """ Self-balancing binary search tree using rebalancing by sub-tree
        rotations of Adelson-Velsky and Landis (AVL).
    """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        BinarySearchTree.__init__(self)

    def get_height(self, current: AVLTreeNode) -> int:
        """
            Get the height of a node. Return current.height if current is 
            not None. Otherwise, return 0.
            :complexity: O(1)
        """

        if current is not None:
            return current.height
        return 0

    def get_num_nodes_subtree(self, current: AVLTreeNode) -> int:
        """
            Get the number of nodes in the subtree. Return current.num_nodes_subtree if current is
            not None. Otherwise, return 0.
            :complexity: O(1)
        """

        if current is not None:
            return current.num_nodes_subtree
        return 0

    def get_balance(self, current: AVLTreeNode) -> int:
        """
            Compute the balance factor for the current sub-tree as the value
            (right.height - left.height). If current is None, return 0.
            :complexity: O(1)
        """

        if current is None:
            return 0
        return self.get_height(current.right) - self.get_height(current.left)

    def insert_aux(self, current: AVLTreeNode, key: K, item: I) -> AVLTreeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert
            it. After insertion, performs sub-tree rotation whenever it becomes
            unbalanced.
            returns the new root of the subtree.
            :complexity best: O(CompK) inserts the item at the root.
            :complexity worst: O(CompK * D) inserting at the bottom of the tree
            where D is the depth of the tree
            CompK is the complexity of comparing the keys
        """
        if current is None:  # base case: at the leaf
            current = AVLTreeNode(key, item)
            self.length += 1
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
        else:  # key == current.key
            raise ValueError('Inserting duplicate item')

        # Update the height of parent node
        current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))

        # Update number of children of the parent node
        current.num_nodes_subtree = 1 + self.get_num_nodes_subtree(current.left) + self.get_num_nodes_subtree(current.right)

        # Rebalance node if needed and return the new root of the subtree
        return self.rebalance(current)


    def delete_aux(self, current: AVLTreeNode, key: K) -> AVLTreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete. After deletion,
            performs sub-tree rotation whenever it becomes unbalanced.
            returns the new root of the subtree.
            :complexity best: O(CompK) deletes root item which does not have a left and/or a right node.
            :complexity worst: O(D) deletes item at the bottom of the tree
            where D is the depth of the tree
            CompK is the complexity of comparing the keys
        """

        if current is None:  # key not found
            raise ValueError('Deleting non-existent item')
        elif key < current.key:
            current.left = self.delete_aux(current.left, key)
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
        else:  # we found our key => do actual deletion
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left

            # general case => find a successor
            succ = self.get_successor(current)
            current.key = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)

        # Update the height of parent node
        current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))

        # Update number of children of the parent node
        current.num_nodes_subtree = 1 + self.get_num_nodes_subtree(current.left) + self.get_num_nodes_subtree(current.right)

        # Rebalance node if needed and return the new root of the subtree
        return self.rebalance(current)

    def left_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform left rotation of the sub-tree.
            Right child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                 current                                       child
                /       \                                      /   \
            l-tree     child           -------->        current     r-tree
                      /     \                           /     \
                 center     r-tree                 l-tree     center

            :complexity: O(1)
        """
        child = current.right
        center = child.left

        # Perform rotation
        child.left = current
        current.right = center

        # Update heights
        current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))
        child.height = 1 + max(self.get_height(child.left), self.get_height(child.right))

        # Update number of children
        current.num_nodes_subtree = 1 + self.get_num_nodes_subtree(current.left) + self.get_num_nodes_subtree(current.right)
        child.num_nodes_subtree = 1 + self.get_num_nodes_subtree(child.left) + self.get_num_nodes_subtree(child.right)

        # Return new root
        return child

    def right_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform right rotation of the sub-tree.
            Left child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                       current                                child
                      /       \                              /     \
                  child       r-tree     --------->     l-tree     current
                 /     \                                           /     \
            l-tree     center                                 center     r-tree

            :complexity: O(1)
        """
        child = current.left
        center = child.right

        # Perform rotation
        child.right = current
        current.left = center

        # Update heights
        current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))
        child.height = 1 + max(self.get_height(child.left), self.get_height(child.right))

        # Update number of children
        current.num_nodes_subtree = 1 + self.get_num_nodes_subtree(current.left) + self.get_num_nodes_subtree(current.right)
        child.num_nodes_subtree = 1 + self.get_num_nodes_subtree(child.left) + self.get_num_nodes_subtree(child.right)

        # Return new root
        return child

    def rebalance(self, current: AVLTreeNode) -> AVLTreeNode:
        """ Compute the balance of the current node.
            Do rebalancing of the sub-tree of this node if necessary.
            Rebalancing should be done either by:
            - one left rotate
            - one right rotate
            - a combination of left + right rotate
            - a combination of right + left rotate
            returns the new root of the subtree.
            :complexity: O(1)
        """
        if self.get_balance(current) >= 2:
            child = current.right
            if self.get_height(child.left) > self.get_height(child.right):
                current.right = self.right_rotate(child)
            return self.left_rotate(current)

        if self.get_balance(current) <= -2:
            child = current.left
            if self.get_height(child.right) > self.get_height(child.left):
                current.left = self.left_rotate(child)
            return self.right_rotate(current)

        return current

    def kth_largest(self, k: int) -> AVLTreeNode:
        """
        Returns the kth largest element in the tree.
        k=1 would return the largest.
        :pre: 0 < k <= the total number of nodes in the tree
        :complexity best: O(1) the kth largest value is the root node
        :complexity worst: O(log(N)) the kth largest value is at the bottom of the tree
        where N is the total number of nodes in the tree

        see kth_largest_aux(self, k: int, current: AVLTreeNode) -> AVLTreeNode
        """
        # precondition: 1 < k <= the number of nodes in the tree
        if k > self.get_num_nodes_subtree(self.root) or k < 1:  # key not found
            raise ValueError('k cannot be greater than the number of elements in the tree and must be greater than 1')

        return self.kth_largest_aux(k, self.root)

    def kth_largest_aux(self, k: int, current: AVLTreeNode) -> AVLTreeNode:
        """
        Find the kth largest value in the subtree
        This is done by determining the number of nodes in each subtree and checking
        whether k must exist to the left or right of a node.

        :complexity best: O(1) the kth largest value is the root node
        :complexity worst: O(log(N)) the kth largest value is at the bottom of the tree
        where N is the total number of nodes in the tree
        Each iteration of kth_largest_in_subtree determines whether the kth largest value is
        the root or if it is in the left or right subtree. So, each iteration divides the subtree
        in half, giving a logN complexity.
        Note: the tree is always balanced - an unbalanced tree would not have this complexity
        """
        num_right_tree_nodes = self.get_num_nodes_subtree(current.right)

        # the kth value is always the one with its right subtree elements == k-1
        if k == num_right_tree_nodes + 1:
            return current
        # if the num elements in the right subtree >= k, move to the right subtree
        elif k <= num_right_tree_nodes:
            return self.kth_largest_aux(k, current.right)
        # otherwise k is in the left subtree. Move to that subtree and update k
        elif k > (num_right_tree_nodes + 1):
            return self.kth_largest_aux(k - num_right_tree_nodes - 1, current.left)

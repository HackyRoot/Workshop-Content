import scrapy
import json


class ReviewHuntSpider(scrapy.Spider):
    name = 'reviewhunt'

    # Zyte API custom settings
    custom_settings = dict(
        DOWNLOAD_HANDLERS = {
            "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
            "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        },
        TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        ZYTE_API_KEY = "YOUR_ZYTE_API_HERE",
        ZYTE_API_TRANSPARENT_MODE= True,
    )

    def start_requests(self):
        url = 'https://www.producthunt.com/frontend/graphql'

        data = {
            "operationName": "ProductReviewsPage",
            "variables": {
                "commentsListSubjectThreadsCursor": "",
                "commentsThreadRepliesCursor": "",
                "slug": "notion",
                "query": None,
                "commentsListSubjectThreadsLimit": 3,
                "includeThreadForCommentId": None,
                "reviewsLimit": 10,
                "reviewsOrder": "HELPFUL",
                "includeReviewId": None,
                "rating": "0",
                "reviewsCursor": "MTA"
            },
        "query": "query ProductReviewsPage($slug:String!$commentsListSubjectThreadsCursor:String=\"\"$commentsListSubjectThreadsLimit:Int!$commentsThreadRepliesCursor:String=\"\"$commentsListSubjectFilter:ThreadFilter$order:ThreadOrder$includeThreadForCommentId:ID$excludeThreadForCommentId:ID$reviewsLimit:Int!$reviewsCursor:String$reviewsOrder:ReviewsOrder$includeReviewId:ID$query:String$rating:String){product(slug:$slug){id slug name reviewsWithBodyCount reviewsRating reviewsCount isMaker isTrashed activeUpcomingEvent{id isFirstLaunch __typename}...ReviewOverallRatingFragment ...ProductReviewsPageReviewsFeedFragment ...ProductReviewsPageAlternativeCardFragment ...ReviewCTAPromptFragment ...StructuredDataFromProduct ...MetaTags __typename}}fragment ProductReviewsPageReviewsFeedFragment on Product{id reviewsCount ...ReviewListFragment __typename}fragment ReviewListFragment on Reviewable{id reviews(first:$reviewsLimit after:$reviewsCursor order:$reviewsOrder includeReviewId:$includeReviewId query:$query rating:$rating){edges{node{id sentiment comment{id bodyHtml __typename}...RatingReviewFragment __typename}__typename}totalCount pageInfo{hasNextPage endCursor __typename}__typename}__typename}fragment RatingReviewFragment on Review{id rating body sentiment user{id username name url isAccountVerified ...JobTitleFragment ...UserImage __typename}comment{id body __typename}post{id name slug __typename}productAnswers{id question{id title path __typename}__typename}...RatingReviewActionBarFragment ...CommentsSubjectFragment __typename}fragment UserImage on User{id name username avatarUrl __typename}fragment CommentsSubjectFragment on Commentable{id canAddCommentReview ...CommentsListSubjectFragment __typename}fragment CommentsListSubjectFragment on Commentable{id threads(first:$commentsListSubjectThreadsLimit after:$commentsListSubjectThreadsCursor filter:$commentsListSubjectFilter order:$order includeCommentId:$includeThreadForCommentId excludeCommentId:$excludeThreadForCommentId){totalCount edges{node{id canAward ...CommentsThreadFragment __typename}__typename}pageInfo{endCursor hasNextPage __typename}__typename}__typename}fragment CommentsThreadFragment on Comment{id isSticky replies(first:5 after:$commentsThreadRepliesCursor allForCommentId:$includeThreadForCommentId){totalCount edges{node{id ...CommentFragment __typename}__typename}pageInfo{endCursor hasNextPage __typename}__typename}...CommentFragment __typename}fragment CommentFragment on Comment{id award badges body bodyHtml canEdit canReply canDestroy canAward createdAt isHidden path isSticky score awardOptions{option __typename}repliesCount subject{id ...on Post{id commentAwardsCount __typename}...on Commentable{id __typename}__typename}user{id headline name firstName username headline ...ComingSoonUserBadgeFragment ...UserImage ...KarmaBadgeFragment __typename}poll{...PollFragment __typename}review{id __typename}...CommentVoteButtonFragment ...FacebookShareButtonFragment __typename}fragment CommentVoteButtonFragment on Comment{id ...on Votable{id hasVoted votesCount __typename}__typename}fragment FacebookShareButtonFragment on Shareable{id url __typename}fragment KarmaBadgeFragment on User{id karmaBadge{kind score __typename}__typename}fragment PollFragment on Poll{id answersCount hasAnswered options{id text imageUuid answersCount answersPercent hasAnswered __typename}__typename}fragment ComingSoonUserBadgeFragment on User{id promotableUpcomingEvent{id __typename}__typename}fragment JobTitleFragment on User{id work{id jobTitle companyName product{id name slug __typename}__typename}__typename}fragment RatingReviewActionBarFragment on Review{id createdAt hasVoted votesCount ...ReviewDeleteButtonFragment ...RatingReviewShareButtonFragment ...RatingReviewEditButtonFragment ...RatingReviewReportButtonFragment ...RatingReviewReplyButtonFragment __typename}fragment ReviewDeleteButtonFragment on Review{id canDestroy __typename}fragment RatingReviewShareButtonFragment on Review{id url user{id name __typename}__typename}fragment RatingReviewEditButtonFragment on Review{id canUpdate product{id name slug __typename}__typename}fragment RatingReviewReportButtonFragment on Review{id __typename}fragment RatingReviewReplyButtonFragment on Review{id product{id isMaker __typename}__typename}fragment ProductReviewsPageAlternativeCardFragment on Product{id slug alternativesCount alternativeAssociations(first:6){edges{node{id alternative:associatedProduct{id slug name tagline ...ProductThumbnailFragment __typename}__typename}__typename}__typename}__typename}fragment ProductThumbnailFragment on Product{id name logoUuid isNoLongerOnline __typename}fragment ReviewOverallRatingFragment on Reviewable{id reviewsWithRatingCount ratingSpecificCount{rating count __typename}__typename}fragment StructuredDataFromProduct on Product{id structuredData __typename}fragment ReviewCTAPromptFragment on Product{id isMaker viewerReview{id __typename}...ReviewCTASharePromptFragment __typename}fragment ReviewCTASharePromptFragment on Product{id name tagline slug ...ProductThumbnailFragment ...FacebookShareButtonFragment __typename}fragment MetaTags on SEOInterface{id meta{canonicalUrl creator description image mobileAppUrl oembedUrl robots title type author authorUrl __typename}__typename}"
        }

        meta={
                "zyte_api_automap": {
                    "httpResponseBody": True,
                },
        }
        headers = {"Content-Type": "application/json"}

        yield scrapy.Request(url=url, method='POST', body=json.dumps(data), headers=headers, callback=self.parse, meta=meta)

    def parse(self, response):
        # parse the response as needed
        print(response.url)
        response_text = json.loads(response.text)

        # Retrieve reviews_cursor from response
        reviews_cursor = response_text['data']['product']['reviews']['pageInfo']['endCursor']
        if reviews_cursor is not None:
            for review in response_text['data']['product']['reviews']['edges']:
                yield {
                    'review': review['node']['body'],
                    'rating': review['node']['rating'],
                    'id': review['node']['id'],
                    'review_url': review['node']['url'],
            }

            data = {
                "operationName": "ProductReviewsPage",
                "variables": {
                    "commentsListSubjectThreadsCursor": "",
                    "commentsThreadRepliesCursor": "",
                    "slug": "notion",
                    "query": None,
                    "commentsListSubjectThreadsLimit": 3,
                    "includeThreadForCommentId": None,
                    "reviewsLimit": 10,
                    "reviewsOrder": "HELPFUL",
                    "includeReviewId": None,
                    "rating": "0",
                    "reviewsCursor": reviews_cursor
                },
                "query": "query ProductReviewsPage($slug:String!$commentsListSubjectThreadsCursor:String=\"\"$commentsListSubjectThreadsLimit:Int!$commentsThreadRepliesCursor:String=\"\"$commentsListSubjectFilter:ThreadFilter$order:ThreadOrder$includeThreadForCommentId:ID$excludeThreadForCommentId:ID$reviewsLimit:Int!$reviewsCursor:String$reviewsOrder:ReviewsOrder$includeReviewId:ID$query:String$rating:String){product(slug:$slug){id slug name reviewsWithBodyCount reviewsRating reviewsCount isMaker isTrashed activeUpcomingEvent{id isFirstLaunch __typename}...ReviewOverallRatingFragment ...ProductReviewsPageReviewsFeedFragment ...ProductReviewsPageAlternativeCardFragment ...ReviewCTAPromptFragment ...StructuredDataFromProduct ...MetaTags __typename}}fragment ProductReviewsPageReviewsFeedFragment on Product{id reviewsCount ...ReviewListFragment __typename}fragment ReviewListFragment on Reviewable{id reviews(first:$reviewsLimit after:$reviewsCursor order:$reviewsOrder includeReviewId:$includeReviewId query:$query rating:$rating){edges{node{id sentiment comment{id bodyHtml __typename}...RatingReviewFragment __typename}__typename}totalCount pageInfo{hasNextPage endCursor __typename}__typename}__typename}fragment RatingReviewFragment on Review{id rating body sentiment user{id username name url isAccountVerified ...JobTitleFragment ...UserImage __typename}comment{id body __typename}post{id name slug __typename}productAnswers{id question{id title path __typename}__typename}...RatingReviewActionBarFragment ...CommentsSubjectFragment __typename}fragment UserImage on User{id name username avatarUrl __typename}fragment CommentsSubjectFragment on Commentable{id canAddCommentReview ...CommentsListSubjectFragment __typename}fragment CommentsListSubjectFragment on Commentable{id threads(first:$commentsListSubjectThreadsLimit after:$commentsListSubjectThreadsCursor filter:$commentsListSubjectFilter order:$order includeCommentId:$includeThreadForCommentId excludeCommentId:$excludeThreadForCommentId){totalCount edges{node{id canAward ...CommentsThreadFragment __typename}__typename}pageInfo{endCursor hasNextPage __typename}__typename}__typename}fragment CommentsThreadFragment on Comment{id isSticky replies(first:5 after:$commentsThreadRepliesCursor allForCommentId:$includeThreadForCommentId){totalCount edges{node{id ...CommentFragment __typename}__typename}pageInfo{endCursor hasNextPage __typename}__typename}...CommentFragment __typename}fragment CommentFragment on Comment{id award badges body bodyHtml canEdit canReply canDestroy canAward createdAt isHidden path isSticky score awardOptions{option __typename}repliesCount subject{id ...on Post{id commentAwardsCount __typename}...on Commentable{id __typename}__typename}user{id headline name firstName username headline ...ComingSoonUserBadgeFragment ...UserImage ...KarmaBadgeFragment __typename}poll{...PollFragment __typename}review{id __typename}...CommentVoteButtonFragment ...FacebookShareButtonFragment __typename}fragment CommentVoteButtonFragment on Comment{id ...on Votable{id hasVoted votesCount __typename}__typename}fragment FacebookShareButtonFragment on Shareable{id url __typename}fragment KarmaBadgeFragment on User{id karmaBadge{kind score __typename}__typename}fragment PollFragment on Poll{id answersCount hasAnswered options{id text imageUuid answersCount answersPercent hasAnswered __typename}__typename}fragment ComingSoonUserBadgeFragment on User{id promotableUpcomingEvent{id __typename}__typename}fragment JobTitleFragment on User{id work{id jobTitle companyName product{id name slug __typename}__typename}__typename}fragment RatingReviewActionBarFragment on Review{id createdAt hasVoted votesCount ...ReviewDeleteButtonFragment ...RatingReviewShareButtonFragment ...RatingReviewEditButtonFragment ...RatingReviewReportButtonFragment ...RatingReviewReplyButtonFragment __typename}fragment ReviewDeleteButtonFragment on Review{id canDestroy __typename}fragment RatingReviewShareButtonFragment on Review{id url user{id name __typename}__typename}fragment RatingReviewEditButtonFragment on Review{id canUpdate product{id name slug __typename}__typename}fragment RatingReviewReportButtonFragment on Review{id __typename}fragment RatingReviewReplyButtonFragment on Review{id product{id isMaker __typename}__typename}fragment ProductReviewsPageAlternativeCardFragment on Product{id slug alternativesCount alternativeAssociations(first:6){edges{node{id alternative:associatedProduct{id slug name tagline ...ProductThumbnailFragment __typename}__typename}__typename}__typename}__typename}fragment ProductThumbnailFragment on Product{id name logoUuid isNoLongerOnline __typename}fragment ReviewOverallRatingFragment on Reviewable{id reviewsWithRatingCount ratingSpecificCount{rating count __typename}__typename}fragment StructuredDataFromProduct on Product{id structuredData __typename}fragment ReviewCTAPromptFragment on Product{id isMaker viewerReview{id __typename}...ReviewCTASharePromptFragment __typename}fragment ReviewCTASharePromptFragment on Product{id name tagline slug ...ProductThumbnailFragment ...FacebookShareButtonFragment __typename}fragment MetaTags on SEOInterface{id meta{canonicalUrl creator description image mobileAppUrl oembedUrl robots title type author authorUrl __typename}__typename}"
            }

            headers = {"Content-Type": "application/json"}
            yield scrapy.Request(url=response.url, method='POST', body=json.dumps(data), headers=headers, callback=self.parse)